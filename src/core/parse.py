from src.core.translate import Translator
from src.util.point import Point
from src.util.amino import Amino


class Parser:
    def __init__(self):
        self.index = None
        self.type = None
        self.chain = None
        self.points = [None, None, None]
        self.aminos = []
        self.trans = Translator()
        self.amino = Amino('', '', 0)
        self.format = ''
        self.split = True

    def format_for(self, file):
        if file.endswith('.cif'):
            return 'cif'
        if file.endswith('.pdb'):
            return 'pdb'
        print('error: unknown file format %s' % file)
        return None

    def read_file(self, file):
        self.format = self.format_for(file)
        with open(file, 'r') as file:
            for line in file:
                self.read_line(line)
        self.flush(self.split)
        self.flush(True)
        return self.aminos

    def read_string(self, string, format):
        self.format = format
        for line in string.split('\n'):
            self.read_line(line)
        self.flush(self.split)
        self.flush(True)
        return self.aminos

    def read_line(self, line):
        if self.format == 'cif':
            line = [v for v in line.split(' ') if v]
        if self.is_chain(line):
            self.add_line(line)

    def flush(self, split):
        polars = self.trans.forward(self.points)
        self.amino.pN = polars[0] if not split else None
        self.amino.pCA = polars[1] if not split else None
        self.amino.is_chain_end = split
        if self.amino.type:
            self.aminos.append(self.amino)
        if self.type:
            self.amino = Amino(self.type, self.chain, self.index)
            self.type = None
            self.index = None
            self.chain = None
            self.amino.set_points(self.points)
            self.amino.is_chain_start = split
            self.points = [None, None, None]
            self.amino.pC = polars[2] if not split else None

    def add_line(self, line):
        type = self.to_type(line)
        index = self.to_index(line)
        chain = self.to_chain(line)
        split = (self.chain != chain)
        if self.index != index or self.chain != chain:
            self.flush(self.split)
            self.split = split
            self.type = type
            self.index = index
            self.chain = chain
        if self.type != type:
            print('error: inconsistent type', self.type, type)
        element = self.to_element(line)
        e = {'N': 0, 'CA': 1, 'C': 2}[element]
        if e is None:
            print('error: unknown element', element)
        if self.points[e]:
            print('error: double element', element)
        self.points[e] = self.to_point(line)

    def is_chain(self, line):
        return self.to_header(line) == 'ATOM' and self.to_element(line) in (
            'N', 'CA', 'C')

    def to_header(self, line):
        if self.format == 'cif':
            return line[0]
        if self.format == 'pdb':
            return line[0:4]

    def to_element(self, line):
        if self.format == 'cif':
            return line[3]
        if self.format == 'pdb':
            return line[13:17].replace(' ', '')

    def to_type(self, line):
        if self.format == 'cif':
            return line[5]
        if self.format == 'pdb':
            return line[17:20].replace(' ', '')

    def to_chain(self, line):
        if self.format == 'cif':
            return line[6]
        if self.format == 'pdb':
            return line[20:22].replace(' ', '')

    def to_index(self, line):
        if self.format == 'cif':
            return int(line[8])
        if self.format == 'pdb':
            return int(line[22:30])

    def to_point(self, line):
        if self.format == 'cif':
            return Point(float(line[10]), float(line[11]), float(line[12]))
        if self.format == 'pdb':
            return Point(
                float(line[30:38]), float(line[38:46]), float(line[46:54]))
