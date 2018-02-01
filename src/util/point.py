import math

# yes, i'm aware of numpy


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def dup(self):
        return Point(self.x, self.y, self.z)

    def is_equal(self, o):
        return isinstance(
            o, Point) and self.x == o.x and self.y == o.y and self.z == o.z

    def __eq__(self, o):
        return self.is_equal(o)

    def is_unequal(self, o):
        return not isinstance(
            o, Point) or self.x != o.x or self.y != o.y or self.z != o.z

    def __ne__(self, o):
        return self.is_unequal(o)

    def is_zero(self):
        return self.x == 0 and self.y == 0 and self.z == 0

    def add(self, o):
        if isinstance(o, Point):
            self.x += o.x
            self.y += o.y
            self.z += o.z
        else:
            self.x += o
            self.y += o
            self.z += o

    def __add__(self, o):
        d = self.dup()
        d.add(o)
        return d

    def __iadd__(self, o):
        self.add(o)
        return self

    def sub(self, o):
        if isinstance(o, Point):
            self.x -= o.x
            self.y -= o.y
            self.z -= o.z
        else:
            self.x -= o
            self.y -= o
            self.z -= o

    def __sub__(self, o):
        d = self.dup()
        d.sub(o)
        return d

    def __isub__(self, o):
        self.sub(o)
        return self

    def mul(self, o):
        if isinstance(o, Point):
            self.x *= o.x
            self.y *= o.y
            self.z *= o.z
        else:
            self.x *= o
            self.y *= o
            self.z *= o

    def __mul__(self, o):
        d = self.dup()
        d.mul(o)
        return d

    def __imul__(self, o):
        self.mul(o)
        return self

    def div(self, o):
        if isinstance(o, Point):
            self.x /= o.x
            self.y /= o.y
            self.z /= o.z
        else:
            self.x /= o
            self.y /= o
            self.z /= o

    def __truediv__(self, o):
        d = self.dup()
        d.div(o)
        return d

    def __itruediv__(self, o):
        self.div(o)
        return self

    def dot(self, o):
        return self.x * o.x + self.y * o.y + self.z * o.z

    def __or__(self, o):
        return self.dot(o)

    def __ior__(self, o):
        raise SyntaxError('%= not supported by Point')

    def cross(self, o):
        x = self.y * o.z - self.z * o.y
        y = self.z * o.x - self.x * o.z
        z = self.x * o.y - self.y * o.x
        self.x = x
        self.y = y
        self.z = z

    def __xor__(self, o):
        d = self.dup()
        d.cross(o)
        return d

    def __ixor__(self, o):
        self.cross(o)
        return self

    def neg(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z

    def __neg__(self):
        d = self.dup()
        d.neg()
        return d

    def lensq(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def length(self):
        return math.sqrt(self.lensq())

    def norm(self):
        if not self.is_zero():
            l = self.length()
            self.x /= l
            self.y /= l
            self.z /= l

    def __invert__(self):
        d = self.dup()
        d.norm()
        return d

    def rotate(self, axis, angle):
        c = math.cos(angle)
        s = math.sin(angle)
        m = 1 - c
        x = self.x * (c + axis.x * axis.x * m) + self.y * (
            axis.x * axis.y * m - axis.z * s) + self.z * (
                axis.x * axis.z * m + axis.y * s)
        y = self.x * (axis.y * axis.x * m + axis.z * s) + self.y * (
            c + axis.y * axis.y * m) + self.z * (
                axis.y * axis.z * m - axis.x * s)
        z = self.x * (axis.z * axis.x * m - axis.y * s) + self.y * (
            axis.z * axis.y * m + axis.x * s) + self.z * (
                c + axis.z * axis.z * m)
        self.x = x
        self.y = y
        self.z = z

    def rotated(self, axis, angle):
        d = self.dup()
        d.rotate(axis, angle)
        return d

    def round(self, ndigits):
        self.x = round(self.x, ndigits)
        self.y = round(self.y, ndigits)
        self.z = round(self.z, ndigits)

    def rounded(self, ndigits):
        d = self.dup()
        d.round(ndigits)
        return d

    def __str__(self):
        return '(%f,%f,%f)' % (self.x, self.y, self.z)

    def __repr__(self):
        return '(%f,%f,%f)' % (self.x, self.y, self.z)
