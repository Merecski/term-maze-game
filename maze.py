from time import sleep

"""
[0][1]--->               0b1000
[1][1,1]          0b0010  [C]  0b0001
 |                       0b0100
 v
Unicode characters: ─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ╵ ╷
"""
walls = {
    0b0000: '  ',
    0b0001: ' ─',
    0b0010: '─ ',
    0b0011: '──',
    0b0100: '╷ ',
    0b0101: '┌─',
    0b0110: '┐ ',
    0b0111: '┬─',
    0b1000: '╵ ',
    0b1001: '└─',
    0b1010: '┘ ',
    0b1011: '┴─',
    0b1100: '│ ',
    0b1101: '├─',
    0b1110: '┤',
    0b1111: '┼─'
}

class Maze:
    def __init__(self, size):
        self.size = size

    def generateMaze(self):
        self.grid = self.generateBlank()
        self.linkCells(self.grid, self.size)

    def generateBlank(self):
        grid = []
        for y in range(self.size):
            tmp = []
            for x in range(self.size):
                tmp.append(Cell())
            grid.append(tmp)
        return grid

    def indexGrid(self, grid, y, x):
        if (y < 0 or x < 0) or (y >= len(grid) or x >= len(grid)):
            return None
        else:
            return grid[y][x]

    def linkCells(self, grid, size):
        for y in range(size):
            for x in range(size):
                grid[y][x].setNeighbor(0b1000, self.indexGrid(grid, y - 1, x))
                grid[y][x].setNeighbor(0b0100, self.indexGrid(grid, y + 1, x))
                grid[y][x].setNeighbor(0b0010, self.indexGrid(grid, y, x - 1))
                grid[y][x].setNeighbor(0b0001, self.indexGrid(grid, y, x + 1))


class Cell:
    def __init__(self):
        self.pos = (0,0)
        self.walls = 0b1111
        self.neighbors = {}

    def setNeighbor(self, face, cell):
        if cell: self.neighbors[face] = cell


if __name__ == '__main__':
    m = Maze(10)
    m.generateMaze()
