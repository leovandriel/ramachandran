import sys
import time
import os
import os.path
import math
import urllib.request


def hook(count, block_size, total_size):
    global last_time
    global last_size
    global last_index
    if count == 0:
        last_time = time.time()
        last_size = block_size
        last_index = 0
        return
    last_size += block_size
    t = time.time()
    if (last_time + 1 < t):
        speed = last_size / (t - last_time)
        sys.stdout.write("%s %.1f KB/s  \r" %
                         (['/', '-', '\\', '|'][last_index % 4], speed / 1000))
        sys.stdout.flush()
        last_time = t
        last_size = 0
        last_index += 1


filetypes = ['pdb', 'cif']
defaultformat = 'pdb'


class Databank:
    def __init__(self, root='data', format=defaultformat):
        self.root = root
        self.format = format

    def path_for(self, name, format=None):
        if format is None: format = self.format
        filename = name.lower() + '.' + format
        filepath = os.path.join(self.root, filename)
        tmp = os.path.join(self.root, '.' + filename + '.downloading')
        if not os.path.exists(self.root):
            os.makedirs(self.root)
        if not os.path.exists(filepath):
            # print('downloading %s ..' % name)
            try:
                urllib.request.urlretrieve(
                    'https://files.rcsb.org/download/' + filename, tmp, hook)
            except urllib.error.HTTPError:
                return
            os.rename(tmp, filepath)
            sys.stdout.write("%s\r" % (' ' * 40))
            sys.stdout.flush()
        return filepath

    def info(self, name, format=None):
        if format is None: format = self.format
        index = 0
        filepath = self.path_for(name, format)
        if filepath is None:
            return
        size = '%.0f Kb' % (os.path.getsize(filepath) / 1000)
        title = None
        with open(filepath, 'r') as file:
            for line in file:
                if format == 'cif':
                    if line.startswith('_struct.title'):
                        title = line[23:].strip()[1:-1]
                if format == 'pdb' and line.startswith('TITLE'):
                    title = line[5:].strip()
                index += 1
                if index > 5000:
                    break
        return title, size

    def list(self):
        names = set()
        for f in os.listdir(self.root):
            if not f.startswith('.') and os.path.isfile(
                    os.path.join(self.root, f)):
                for type in filetypes:
                    if f.endswith('.' + type):
                        names.add(f[:-1 - len(type)])
        return sorted(list(names))

    def types():
        return filetypes
