class frange:
    def __init__(self, start, stop=None, step=1.0):
        if stop is None:
            self.start = 0.0
            self.stop = float(start)
        else:
            self.start = float(start)
            self.stop = float(stop)
        self.step = float(step)
        self.current = self.start

    def __iter__(self):
        return self

    def __next__(self):
        if (self.step > 0 and self.current >= self.stop) or (self.step < 0 and self.current <= self.stop):
            raise StopIteration
        current = self.current
        self.current += self.step
        return current


for i in frange(1, 100, 3.5):
    print(i)

assert (list(frange(5)) == [0, 1, 2, 3, 4])
assert (list(frange(2, 5)) == [2, 3, 4])
assert (list(frange(2, 10, 2)) == [2, 4, 6, 8])
assert (list(frange(10, 2, -2)) == [10, 8, 6, 4])
assert (list(frange(2, 5.5, 1.5)) == [2, 3.5, 5])
assert (list(frange(1, 5)) == [1, 2, 3, 4])
assert (list(frange(0, 5)) == [0, 1, 2, 3, 4])
assert (list(frange(0, 0)) == [])
assert (list(frange(100, 0)) == [])

print('SUCCESS!')


class colorizer:
    COLORS = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'white': '\033[97m',
        'reset': '\033[0m',
    }

    def __init__(self, color):
        self.color = self.COLORS[color]

    def __enter__(self):
        print(self.color, end='')

    def __exit__(self):
        print(self.COLORS['reset'], end='')


print('\033[93m', end='')
print('aaa')
print('bbb')
print('\033[0m', end='')
print('ccc')

print('printed in default color')

with colorizer('blue'):
    print('This is yellow text')
