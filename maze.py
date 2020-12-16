import random
import time
import sys

"""
[0][1]--->               0b1000
[1][1,1]          0b0010  [C]  0b0001
 |                       0b0100
 v
Unicode characters: ─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼
"""
gui_encode = {
    0b0000: '  ',
    0b0001: ' ─',
    0b0010: '─ ',
    0b0011: '──',
    0b0100: '┬ ',
    0b0101: '┌─',
    0b0110: '┐ ',
    0b0111: '┬─',
    0b1000: '┴ ',
    0b1001: '└─',
    0b1010: '┘ ',
    0b1011: '┴─',
    0b1100: '│ ',
    0b1101: '├─',
    0b1110: '┤ ',
    0b1111: '┼─'
}


class Maze:
    def __init__(self, size, animate_fps=0):
        self.animate = (animate_fps > 0)
        self.animate_fps = animate_fps
        self.size = size
        self.start = (0, random.randint(0, self.size - 1))
        self.end =   (self.size - 1, random.randint(0, self.size - 1))
        self.grid = []

    def __str__(self):
        string = '  ' * self.start[1] + 'S\n'
        for row in self.grid:
            tmp = ''
            for cell in row:
                tmp += gui_encode[cell.walls ^ 0b1111]
            string += tmp + '\n'
        string += '  ' * self.end[1] + 'E'
        return string

    def returnCell(self, pos):
        return self.grid[pos[0]][pos[1]]

    def algorithmInit(self):
        root = self.returnCell(self.start)
        root.knockWalls(0b1000)
        main_cell_stack = [root]
        while main_cell_stack:
            cell = random.choice(main_cell_stack)
            if cell.hasNeighbors():
                main_cell_stack += (self.algorithmShortWalk(cell))
            else:
                main_cell_stack.remove(cell)

    def algorithmShortWalk(self, root):
        max_trail = 2 * self.size // 3
        cell_stack = [root]
        while cell_stack and len(cell_stack) < max_trail:
            free_cells = cell_stack[-1].hasNeighbors()
            curr_cell = cell_stack[-1]
            if free_cells:
                if self.animate:
                    print(str(self) + '\n' + '\033[' + str(self.size +3) + 'F')
                    time.sleep(self.animate_fps)
                face, next_cell = random.choice(free_cells)
                curr_cell.knockWalls(face)
                if next_cell == self.returnCell(self.end):
                    next_cell.knockWalls(0b0100)
                    return cell_stack
                else:
                    cell_stack.append(next_cell)
            else:
                cell_stack.pop()
        return cell_stack

    def indexGrid(self, grid, y, x):
        if (y < 0 or x < 0) or (y >= len(grid) or x >= len(grid)):
            return None
        else:
            return grid[y][x]

    def generateBlank(self, grid):
        for y in range(self.size):
            tmp = []
            for x in range(self.size):
                tmp.append(Cell())
            grid.append(tmp)

    def generateMaze(self):
        self.generateBlank(self.grid)
        self.linkCells(self.grid, self.size)
        self.algorithmInit()

    def linkCells(self, grid, size):
        for y in range(size):
            for x in range(size):
                grid[y][x].setNeighbor(0b1000, self.indexGrid(grid, y - 1, x))
                grid[y][x].setNeighbor(0b0100, self.indexGrid(grid, y + 1, x))
                grid[y][x].setNeighbor(0b0010, self.indexGrid(grid, y, x - 1))
                grid[y][x].setNeighbor(0b0001, self.indexGrid(grid, y, x + 1))


class Cell:
    def __init__(self):
        self.walls = 0b1111
        self.neighbors = {}

    def setNeighbor(self, face, cell):
        if cell: self.neighbors[face] = cell

    def hasNeighbors(self):
        avaliable = []
        for face, cell in self.neighbors.items():
            if cell.isEmpty():
                avaliable.append((face, cell))
        return avaliable

    def isEmpty(self):
        return self.walls == 0b1111

    def knockWalls(self, wall):
        self.walls ^= wall
        if wall > 0b0010:
            inv_wall = 0b1100 ^ wall
        else:
            inv_wall = 0b0011 ^ wall
        if wall in self.neighbors:
            self.neighbors[wall].walls ^= inv_wall


if __name__ == '__main__':
    size = 10
    animate_fps = 0
    try:
        size = int(sys.argv[1])
        animate_fps = float(sys.argv[2])
    except IndexError: pass
    m = Maze(size, animate_fps)
    try: m.generateMaze()
    except KeyboardInterrupt: pass
    print(m)
