from plexer import LexError, TYPE, tokenize

# member variables.
PARSERS = { }

#-------------------
# register_parser(some_parser, ['ext1', 'ext2'])
#-------------------
def register_parser(file_extensions, parser):
    """Associate a parser with a list of file extensions."""

    if isinstance(file_extensions, str):
        file_extensions = [file_extensions]

    for ext in file_extensions:
        if PARSERS.get(ext):
            print 'WARNING: PARSERS[' + ext + '] is being replaced.'
        PARSERS[ext] = parser

# alias.
add_parser = register_parser

#==============================================================================
# ParseError
#==============================================================================
class ParseError(Exception):

    def __init__(self, msg, ctx={}):
        self.msg = msg

        if 'token' in ctx:
            self.token = ctx['token']

    def __str__(self):
        return self.msg

#==============================================================================
# Parser
#==============================================================================
class Parser:
    """Determines how to parse the tokens."""

    def __init__(self, lexer):
        self.lexer = lexer
        self._specs = {}

    def add_spec(self, name, spec):
        self._specs[name] = spec

    def parse(self, tokens, end, ctx):
        for name,spec in self._specs.iteritems():
            elem = spec.parse(tokens, end, ctx)
            if elem != None:
                return elem
        return None

#==============================================================================
# Helper Functions
#==============================================================================
def _eof(at, tokens, end, ctx, idx):
    raise ParseError('EOF at ' + at, ctx)

def _eat_whitespace(tokens, end, idx):
    if tokens[idx]['type'] == TYPE.WHITESPACE:
        return idx + 1
    return idx


#******************************************************************************
# C Parser
#******************************************************************************

#==============================================================================
# CInclude
#==============================================================================

class CInclude:
    """Parses an include statement."""

    @staticmethod
    def _sanitize_file_name(filename):
        filename = filename.strip()
        if len(filename) >= 2:
            if filename[0] == '"' and filename[-1] == '"':
                return CInclude._sanitize_file_name(filename[1:-1])
        return filename

    def __init__(self, file, is_local):
        self.name = 'include'
        self.file = CInclude._sanitize_file_name(file)
        self.is_local = is_local

    def __str__(self):
        if self.is_local:
            return '#include "' + self.file + '"'
        else:
            return '#include <' + self.file + '>'

    @staticmethod
    def parse(tokens, end, ctx):
        idx = ctx['idx']

        if tokens[idx]['value'] != '#include':
            return None

        idx = _eat_whitespace(tokens, end, idx + 1)
        if idx >= end:
            raise ParseError('EOF at #include', ctx)

        if tokens[idx]['type'] == TYPE.STRING:
            ctx['idx'] = idx + 1
            return CInclude(tokens[idx]['value'], is_local=True)

        if tokens[idx]['value'] != '<':
            raise ParseError('Invalid statement: #include ' +
                             tokens[idx]['value'], ctx)

        idx = idx + 1
        path = []
        while True:
            if idx >= end:
                raise ParseError('EOF at #include', ctx)

            if tokens[idx]['type'] == TYPE.NEWLINE:
                raise ParseError('Invalid #include statement', ctx)

            val = tokens[idx]['value']
            idx = idx + 1
            if val == '>':
                break

            path.append(val)

        ctx['idx'] = idx
        return CInclude(''.join(path), is_local=False)


# associate the C parser with various filetypes.
c_parser = Parser('c')
c_parser.add_spec('include', CInclude)
add_parser(['c', 'cpp'], c_parser)

#******************************************************************************
# parse
#******************************************************************************

def parse(s, parser='c'):

    # lookup parser.
    ext = parser.lower()
    if not ext in PARSERS:
        raise ParseError("No parser associated with '" + ext + "', use add_parser")
    parser = PARSERS[ext]

    # tokenize the string.
    tokens = tokenize(s, parser.lexer)
    elems = []

    ctx = {}
    ctx['tokens'] = tokens
    ctx['idx'] = 0
    end = len(tokens)
    ctx['end'] = end

    while ctx['idx'] < end:
        elem = parser.parse(tokens, end, ctx)
        if elem != None:
            elems.append(elem)
        else:
            ctx['idx'] = ctx['idx'] + 1

    return elems
