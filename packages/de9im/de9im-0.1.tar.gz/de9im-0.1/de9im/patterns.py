
DIMS = {
    'F': frozenset('F'),
    'T': frozenset('012'),
    '*': frozenset('F012'),
    '0': frozenset('0'),
    '1': frozenset('1'),
    '2': frozenset('2'),
    }

def pattern(pattern_string):
    return Pattern(pattern_string)

class Pattern(object):
    def __init__(self, pattern_string):
        self.pattern = tuple(pattern_string.upper())
    def __str__(self):
        return ''.join(self.pattern)
    def __repr__(self):
        return "DE-9IM pattern: '%s'" % str(self)
    def matches(self, matrix_string):
        matrix = tuple(matrix_string.upper())
        def onematch(p, m):
            return m in DIMS[p]
        return bool(
            reduce(lambda x, y: x * onematch(*y), zip(self.pattern, matrix), 1)
            )

class AntiPattern(object):
    def __init__(self, anti_pattern_string):
        self.anti_pattern = tuple(anti_pattern_string.upper())
    def __str__(self):
        return '!' + ''.join(self.anti_pattern)
    def __repr__(self):
        return "DE-9IM anti-pattern: '%s'" % str(self)
    def matches(self, matrix_string):
        matrix = tuple(matrix_string.upper())
        def onematch(p, m):
            return m in DIMS[p]
        return not (
            reduce(lambda x, y: x * onematch(*y), 
                   zip(self.anti_pattern, matrix),
                   1)
            )

class NOrPattern(object):
    def __init__(self, pattern_strings):
        self.patterns = [tuple(s.upper()) for s in pattern_strings]
    def __str__(self):
        return '||'.join([''.join(list(s)) for s in self.patterns])
    def __repr__(self):
        return "DE-9IM or-pattern: '%s'" % str(self)
    def matches(self, matrix_string):
        matrix = tuple(matrix_string.upper())
        def onematch(p, m):
            return m in DIMS[p]
        for pattern in self.patterns:
            val = bool(
                reduce(lambda x, y: x * onematch(*y), zip(pattern, matrix), 1))
            if val is True:
                break
        return val
    

# Familiar names for patterns or patterns grouped in logical expression
# ---------------------------------------------------------------------
contains = Pattern('T*****FF*')
# cross_lines is only valid for pairs of lines and/or multi-lines
crosses_lines = Pattern('0********')
# following are valid for mixed types
crosses_point_line = crosses_point_region = crosses_line_region = Pattern(
                                                            'T*T******')
disjoint = Pattern('FF*FF****')
equal = Pattern('T*F**FFF*')
intersects = AntiPattern('FF*FF****')
# points and regions share an overlap pattern
overlaps_points = overlaps_regions = Pattern('T*T***T**')
# following is valid for lines only
overlaps_lines = Pattern('1*T***T**')
touches = NOrPattern(['FT*******', 'F**T*****', 'F***T****'])
within = Pattern('T*F**F***')


