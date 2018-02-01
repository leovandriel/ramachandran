import math
from src.util.point import Point


class Translator:
    def __init__(self):
        self.pos = Point(1, 0, 0)
        self.dir = Point(0, 1, 0)
        self.ori = Point(0, 0, 1)

    def forward_step(self, point):
        if not point:
            return None
        new_pos = point
        new_dir = new_pos - self.pos
        delta = new_dir.length()
        if new_dir.is_zero():
            new_dir = self.dir
        else:
            new_dir.norm()
        new_ori = new_dir ^ self.dir
        if new_ori.is_zero():
            new_ori = self.ori
        else:
            new_ori.norm()
        beta = 180 - math.acos(new_dir | self.dir) * 180 / math.pi
        alpha = -math.acos(new_ori | self.ori) * 180 / math.pi
        if (new_ori ^ self.ori) | self.dir < 0:
            alpha = -alpha
        self.pos = new_pos
        self.dir = new_dir
        self.ori = new_ori
        return Point(alpha, beta, delta)

    def forward(self, point):
        if isinstance(point, list):
            return list(map(lambda p: self.forward_step(p), point))
        else:
            return self.forward_step(point)

    def backward_step(self, polar):
        if not polar:
            return None
        alpha = polar.x
        beta = polar.y
        delta = polar.z
        new_ori = self.ori.rotated(self.dir, alpha * math.pi / 180)
        new_dir = self.dir.rotated(new_ori, -(180 - beta) * math.pi / 180)
        new_pos = self.pos + new_dir * delta
        self.pos = new_pos
        self.dir = new_dir
        self.ori = new_ori
        return new_pos

    def backward(self, polar):
        if isinstance(polar, list):
            return list(map(lambda p: self.backward_step(p), polar))
        else:
            return self.backward_step(polar)
