from src.util.point import Point

char_lookup = {
    'ALA': 'A',
    'ARG': 'R',
    'ASN': 'N',
    'ASP': 'D',
    'CYS': 'C',
    'GLN': 'Q',
    'GLU': 'E',
    'GLY': 'G',
    'HIS': 'H',
    'ILE': 'I',
    'LEU': 'L',
    'LYS': 'K',
    'MET': 'M',
    'PHE': 'F',
    'PRO': 'P',
    'SER': 'S',
    'THR': 'T',
    'TRP': 'W',
    'TYR': 'Y',
    'VAL': 'V',
}

name_lookup = {
    'ALA': 'Alanine',
    'ARG': 'Arginine',
    'ASN': 'Asparagine',
    'ASP': 'Aspartic acid',
    'ASP': 'Aspartic',
    'CYS': 'Cysteine',
    'GLN': 'Glutamine',
    'GLU': 'Glutamic acid',
    'GLU': 'Glutamic',
    'GLY': 'Glycine',
    'HIS': 'Histidine',
    'ILE': 'Isoleucine',
    'LEU': 'Leucine',
    'LYS': 'Lysine',
    'MET': 'Methionine',
    'PHE': 'Phenylalanine',
    'PRO': 'Proline',
    'SER': 'Serine',
    'THR': 'Threonine',
    'TRP': 'Tryptophan',
    'TYR': 'Tyrosine',
    'VAL': 'Valine',
}

code_lookup = {}
for code in char_lookup:
    code_lookup[char_lookup[code].lower()] = code
for code in name_lookup:
    code_lookup[name_lookup[code].lower()] = code


class Amino:
    def __init__(self, type, chain, index):
        self.type = type
        self.chain = chain
        self.index = index
        self.is_chain_start = False
        self.is_chain_end = False

    def points(self):
        return [self.N, self.CA, self.C]

    def set_points(self, points):
        self.N = points[0]
        self.CA = points[1]
        self.C = points[2]

    def polars(self):
        return [self.pN, self.pCA, self.pC]

    def set_polars(self, polars):
        self.pN = polars[0]
        self.pCA = polars[1]
        self.pC = polars[2]

    def alphas(self):
        return Point(self.pN.x, self.pCA.x, self.pC.x)

    def betas(self):
        return Point(self.pN.y, self.pCA.y, self.pC.y)

    def deltas(self):
        return Point(self.pN.z, self.pCA.z, self.pC.z)

    def phi(self):
        return self.pC.x if self.pC is not None else None

    def psi(self):
        return self.pN.x if self.pN is not None else None

    def omega(self):
        return self.pCA.x if self.pCA is not None else None

    def endstr(self):
        if self.is_chain_start and self.is_chain_end:
            return 'SE'
        if self.is_chain_start:
            return 'S'
        if self.is_chain_end:
            return 'E'
        return 'M'

    def code_for(name):
        if name is None:
            return None
        if name.upper() in name_lookup:
            return name.upper()
        return code_lookup.get(name.lower(), None)

    def name_for(name):
        return name_lookup.get(Amino.code_for(name), None)

    def char_for(name):
        return char_lookup.get(Amino.code_for(name), None)

    def __str__(self):
        return '(%s,%s,%s,%s,%s,%s,%s)' % (self.type, self.chain, self.index,
                                           self.N, self.CA, self.C,
                                           self.endstr())

    def __repr__(self):
        return '(%s,%s,%s,%s,%s,%s,%s)' % (self.type, self.chain, self.index,
                                           self.N, self.CA, self.C,
                                           self.endstr())
