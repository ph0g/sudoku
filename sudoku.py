from math import isqrt

class SudokuGrid:
    def __init__(self, builder):
        self._size = builder.size
        self._grid = builder.grid

    @staticmethod
    def from_array(array_of_values):
        builder = SudokuGrid.Builder(size=len(array_of_values))
        for i, row in enumerate(array_of_values):
            for j, value in enumerate(row):
                if value == 0:
                    continue
                builder.set(value, row_index=i, column_index=j)
        return builder.build()


    @property
    def size(self):
        return self._size

    @property
    def grid(self):
        return self._grid.copy()

    def __str__(self):
        s = ''
        value_string_max_length = len(str(self.size))
        for i in range(self.size):
            s += ('+' + '-'*value_string_max_length)*self.size + '+\n'
            s += ('+' + '|'.join([f'{self._grid[i][j]:{value_string_max_length}}'
                                  if self._grid[i][j] != 0 else ' '*value_string_max_length for j in range(self.size)])
                  + '+\n')
        return s + ('+' + '-'*value_string_max_length)*self.size + '+'

    class Builder:
        def __init__(self, size=9):
            if size > 3:
                n = isqrt(size)
                if n * n != size:
                    raise ValueError('size must be a square number.')
                self._size = size
            else:
                raise ValueError('size must be > 3.')

            self._grid = [[0 for _ in range(size)] for _ in range(size)]

        @property
        def size(self):
            return self._size

        @property
        def grid(self):
            return self._grid.copy()

        def _check_index(self, index):
            if index not in range(self._size):
                raise ValueError(f'index must be between 0 and {self._size-1}.')

        def _row_contains(self, row_index, value):
            for i in range(self._size):
                if self._grid[row_index][i] == value:
                    return True
            return False

        def _column_contains(self, column_index, value):
            for i in range(self._size):
                if self._grid[i][column_index] == value:
                    return True
            return False

        def _get_area_index(self, row_index, column_index):
            n = isqrt(self.size)
            return row_index//n*n + column_index//n

        def _get_area_center_coordinates(self, area_index):
            n = isqrt(self._size)
            return area_index//n*n + n//2, area_index%n*n + n//2

        def _area_contains(self, area_index, value):
            n = isqrt(self.size)//2
            x, y = self._get_area_center_coordinates(area_index)
            for i in range(-n, n+1):
                for j in range(-n, n+1):
                    if self._grid[x+i][y+j] == value:
                        return True
            return False

        def set(self, value, row_index, column_index):
            self._check_index(row_index)
            self._check_index(column_index)
            if self._grid[row_index][column_index] == 0:
                if value in range(1, self._size + 1):
                    if self._row_contains(row_index, value):
                        raise ValueError(f'Value {value} is already present in the row {column_index}.')
                    if self._column_contains(column_index, value):
                        raise ValueError(f'Value {value} is already present in the column {column_index}.')
                    area_index = self._get_area_index(row_index, column_index)
                    if self._area_contains(area_index, value):
                        raise ValueError(f'Value {value} is already present in the area {area_index}.')
                    self._grid[row_index][column_index] = value
                else:
                    raise ValueError(f'value must be between 1 and {self._size + 1}')
            else:
                raise IndexError(f'Cell ({row_index}, {column_index}) has already been set.')
            return self

        def build(self):
            return SudokuGrid(self)


if __name__ == '__main__':
    sudoku_grid = SudokuGrid.Builder(size=16)\
                            .set(2, 5, 3)\
                            .set(16, 6, 0)\
                            .set(11, 8, 8)\
                            .build()
    print(sudoku_grid)

    array = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 5, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 7, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 8, 0],
             [9, 0, 0, 0, 0, 0, 0, 0, 1],
            ]

    sudoku_grid_2 = SudokuGrid.from_array(array)
    print(sudoku_grid_2)