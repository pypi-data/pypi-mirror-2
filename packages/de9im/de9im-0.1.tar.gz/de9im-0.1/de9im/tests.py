import unittest

from de9im import pattern
from de9im.patterns import contains, within, crosses_lines, crosses_point_line
from de9im.patterns import disjoint, equal, intersects, touches
from de9im.patterns import overlaps_points, overlaps_lines, overlaps_regions

class TestPatternRepr:
    def test(self):
        pat = pattern('T*F**F***')
        assert str(pat) == 'T*F**F***'
        assert repr(pat) == "DE-9IM pattern: 'T*F**F***'"

class TestPatternMatch:
    def test(self):
        pat = pattern('T*F**F***')
        assert pat.matches('10F00F000') == True
        assert pat.matches('F0F00F000') == False

class TestContainsMatch:
    def test(self):
        assert contains.matches('10F00FFF0') == True
        assert contains.matches('F0F00F000') == False

class TestLineCrossMatch:
    def test(self):
        assert crosses_lines.matches('00F00FFF0') == True
        assert crosses_lines.matches('10F00F000') == False

class TestOtherCrossMatch:
    def test(self):
        assert crosses_point_line.matches('10100FFF0') == True
        assert crosses_lines.matches('10F00F000') == False

class TestDisjointMatch:
    def test(self):
        assert disjoint.matches('FF0FF0000') == True
        assert disjoint.matches('0F0FF0000') == False

class TestEqualMatch:
    def test(self):
        assert equal.matches('10F00FFF0') == True
        assert equal.matches('10100FFF0') == False

class TestIntersectsMatch:
    def test(self):
        assert repr(intersects) == "DE-9IM anti-pattern: '!FF*FF****'"
        assert intersects.matches('FF0FF0000') == False
        assert intersects.matches('0F0FF0000') == True

class TestOverlapPointsMatch:
    def test(self):
        assert overlaps_points.matches('101000100') == True
        assert overlaps_points.matches('F01000100') == False

class TestOverlapLinesMatch:
    def test(self):
        assert overlaps_lines.matches('101000100') == True
        assert overlaps_lines.matches('201000100') == False

class TestTouchMatch1(unittest.TestCase):
    def test(self):
        self.failUnlessEqual(repr(touches), "DE-9IM or-pattern: 'FT*******||F**T*****||F***T****'")
        assert touches.matches('FF0100000') == True
        assert touches.matches('101000100') == False

class TestWithinMatch:
    def test(self):
        assert within.matches('10F00F000') == True
        assert within.matches('F0F00F000') == False


