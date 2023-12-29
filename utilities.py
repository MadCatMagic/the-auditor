from typing import TypeVar, Callable, Any
T = TypeVar('T')
def pprintMatrix(matrix: list[list[T]], prefix: str = "", spaces: int = 0, converter: Callable[[T], str] = str, returnAsString: bool = False) -> None | str:
    s = [[converter(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = (" " * spaces).join('{{:{}}}'.format(x) for x in lens)
    table = [prefix + fmt.format(*row) for row in s]
    res = '\n'.join(table)
    if returnAsString:
        return res
    print(res)

def splitIntoArray(array: list[Any], every: int) -> list[list[Any]]:
    arr = []
    for i in range(len(array) // every + 1):
        t = [v[1] for v in zip(range(every), array[i * every : i * every + every])]
        if t != []:
            arr.append(t)
    return arr

class counter:
    def __init__(self):
        self._dict = {}

    def count(self, obj, num = 1):
        if obj in self._dict:
            self._dict[obj] += num
        else:
            self._dict[obj] = num

    def __iter__(self):
        return iter(self._dict.items())
    
    def __len__(self):
        return len(self._dict)
    
    def sum(self) -> int:
        return sum(self._dict.values())