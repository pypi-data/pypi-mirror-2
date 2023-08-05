import csv
import sys
import re 
import os.path
import operator
import itertools
import copy
import logging
log = logging.getLogger('pydap')

from pydap.model import *
from pydap.model import SequenceData
from pydap.proxy import ConstraintExpression
from pydap.responses.das import typeconvert
from pydap.lib import combine_slices, fix_slice
from pydap.util.safeeval import expr_eval
from pydap.handlers.lib import BaseHandler
from pydap.exceptions import OpenFileError, ConstraintExpressionError


class Handler(BaseHandler):

    extensions = re.compile(r"^.*\.csv$", re.IGNORECASE)

    def __init__(self, filepath):
        self.filepath = filepath

    def parse_constraints(self, environ):
        try:
            fp = open(self.filepath, 'Ur')
            reader = csv.reader(fp)
        except:
            message = 'Unable to open file %s.' % self.filepath
            raise OpenFileError(message)

        # Build the dataset object.
        dataset = DatasetType(os.path.split(self.filepath)[1])

        # Build the sequence object, and insert it in the dataset.
        seq = SequenceType('sequence')
        dataset[seq.name] = seq

        # Parse the constraint expression from ``environ['pydap.ce']``,
        # extracting the requested fields, any filters (queries) and the
        # slice for the sequence.
        fields, queries = environ['pydap.ce']
        queries = filter(bool, queries)  # fix for older version of pydap
        all_vars = reader.next()
        slices = [f[0][1] for f in fields if f[0][0] == seq.name]
        if slices:
            slice_ = slices[0]
        else:
            slice_ = None
        # Check that all slices are equal. 
        if [s for s in slices if s != slice_]:
            raise ConstraintExpressionError('Slices are not unique!')
        # If no fields have been explicitly requested, of if the sequence
        # has been requested directly, return all variables.
        if not fields or seq.name in [f[0][0] for f in fields if len(f) == 1]:
            fields = [[(name, ())] for name in all_vars]

        # Peek first line for types.
        first_line = reader.next()
        fp.close()
        types_ = [typeconvert(lazy_eval(col)) for col in first_line]

        # Add all requested variables to the sequence.
        cols = []
        for var in fields:
            while var:
                name, unused_slice = var.pop(0)
                if name == seq.name:
                    continue
                elif name in all_vars:
                    cols.append(name)
                    type_ = types_[ all_vars.index(name) ]
                    seq[name] = BaseType(name=name, type=type_)
                else:
                    raise ConstraintExpressionError('Invalid token: "%s"' % name)

        # Add a proxy to the data.
        seq.data = CSVProxy(self.filepath, seq.id, tuple(cols), queries, slice_)
        return dataset


class CSVProxy(SequenceData):
    """
    A ``SequenceData`` object that reads data from a CSV file.

    """
    def __init__(self, filepath, id, cols, queries, slice_=None):
        self.filepath = filepath
        self.id = id
        self.cols = cols
        self.queries = queries
        self._slice = slice_ or (slice(None),)

    def __deepcopy__(self, memo=None, _nil=[]):
        out = self.__class__(self.filepath, self.id,
                self.cols[:], self.queries[:], self._slice)
        return out

    def __getitem__(self, key):
        out = copy.deepcopy(self)
        if isinstance(key, ConstraintExpression):
            out.queries.append(str(key))
        elif isinstance(key, basestring):
            out._slice = (slice(None),)
            out.id = '%s.%s' % (self.id, key)
            out.cols = out.id
        elif isinstance(key, tuple):
            out.cols = tuple( '%s.%s' % (self.id, col)
                    for col in key )
        else:
            out._slice = combine_slices(self._slice, fix_slice(key, (sys.maxint,)))
        return out

    def __iter__(self):
        try:
            fp = open(self.filepath, 'Ur')
            reader = csv.reader(fp)
        except:
            message = 'Unable to open file %s.' % self.filepath
            raise OpenFileError(message)

        # get requested vars
        all_vars = reader.next()
        if isinstance(self.cols, tuple):
            cols = self.cols
        else:
            cols = (self.cols,)
        indexes = [ all_vars.index(col) for col in cols ]

        # get data 
        data = itertools.imap(lambda line: map(lazy_eval, line), reader)

        # filter according to CE, return only selected vars and slice
        data = itertools.ifilter(build_filter(self.queries, all_vars), data)
        data = itertools.imap(lambda line: [ line[i] for i in indexes ], data)
        data = itertools.islice(data, self._slice[0].start, self._slice[0].stop, self._slice[0].step)

        if not isinstance(self.cols, tuple):
            data = itertools.imap(operator.itemgetter(0), data)

        def output():
            for line in data: yield line
            fp.close()

        return output()

    # Comparisons return a ``ConstraintExpression`` object
    def __eq__(self, other): return ConstraintExpression('%s=%s' % (self.id, other))
    def __ne__(self, other): return ConstraintExpression('%s!=%s' % (self.id, other))
    def __ge__(self, other): return ConstraintExpression('%s>=%s' % (self.id, other))
    def __le__(self, other): return ConstraintExpression('%s<=%s' % (self.id, other))
    def __gt__(self, other): return ConstraintExpression('%s>%s' % (self.id, other))
    def __lt__(self, other): return ConstraintExpression('%s<%s' % (self.id, other))


def build_filter(queries, vars_):
    """This function is a filter builder.

    Given a list of DAP formatted queries and a list of variable names,
    this function returns a dynamic filter function to filter rows.

    From the example in the DAP specification:

        >>> vars_ = ['index', 'temperature', 'site']
        >>> data = []
        >>> data.append([10, 17.2, 'Diamond_St'])
        >>> data.append([11, 15.1, 'Blacktail_Loop'])
        >>> data.append([12, 15.3, 'Platinum_St'])
        >>> data.append([13, 15.1, 'Kodiak_Trail'])

    Rows where index is greater-than-or-equal 11:

        >>> f = build_filter(['index>=11'], vars_)
        >>> for line in itertools.ifilter(f, data):
        ...     print line
        [11, 15.1, 'Blacktail_Loop']
        [12, 15.300000000000001, 'Platinum_St']
        [13, 15.1, 'Kodiak_Trail']

    Rows where site ends with '_St':

        >>> f = build_filter(['site=~".*_St"'], vars_)
        >>> for line in itertools.ifilter(f, data):
        ...     print line
        [10, 17.199999999999999, 'Diamond_St']
        [12, 15.300000000000001, 'Platinum_St']

    Index greater-or-equal-than 11 AND site ends with '_St':

        >>> f = build_filter(['site=~".*_St"', 'index>=11'], vars_)
        >>> for line in itertools.ifilter(f, data):
        ...     print line
        [12, 15.300000000000001, 'Platinum_St']

    Python is great, isn't it? :)

    """
    filters = [bool]
    p = re.compile(r'''^                          # Start of selection
                       (?P<var1>.*?)              # Anything
                       (?P<op><=|>=|!=|=~|>|<|=)  # Operators
                       (?P<var2>.*?)              # Anything
                       $                          # EOL
                    ''', re.VERBOSE)

    for query in queries:
        m = p.match(query)
        if not m: raise ConstraintExpressionError('Invalid constraint expression: %s.' % query)

        # Functions associated with each operator.
        op = {'<' : operator.lt,
              '>' : operator.gt,
              '!=': operator.ne,
              '=' : operator.eq,
              '>=': operator.ge,
              '<=': operator.le,
              '=~': lambda a,b: re.match(b, a),
             }[m.group('op')]

        # Strip queries of sequence id.
        a = m.group('var1')
        if a.startswith('sequence.'): a = a[9:]
        b = m.group('var2')
        if b.startswith('sequence.'): b = b[9:]

        # Build the filter for the first variable.
        if a in vars_:
            var1 = operator.itemgetter( vars_.index(a) )

            # Build the filter for the second variable. It could be either
            # a name or a constant.
            if b in vars_:
                var2 = operator.itemgetter( vars_.index(b) )
            else:
                var2 = lambda x, b=b: expr_eval(b)

            # This is the filter. We apply the function (op) to the variable
            # filters (var1 and var2).
            filter0 = lambda x, op=op, var1=var1, var2=var2: op(var1(x), var2(x))
            filters.append(filter0)

    return lambda line: reduce(lambda x,y: x and y, [f(line) for f in filters])


def lazy_eval(s):
    """Try to evalute expression or fallback to string.
    
        >>> lazy_eval("1")
        1
        >>> lazy_eval("None")

    """
    try:
        s = expr_eval(s)
    except:
        pass
    return s


if __name__ == '__main__':
    import sys
    from paste.httpserver import serve

    application = Handler(sys.argv[1])
    serve(application, port=8001)
