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
        return self.gridToString(self.grid)

    def gridToString(self, grid):
        string = '\033[1m  ' * self.start[1] + 'S\n'
        for row in grid:
            tmp = ''
            for cell in row:
                if cell.solution:
                    tmp += '\033[34m' + gui_encode[cell.walls ^ 0b1111] + '\033[0m'
                else:
                    tmp += gui_encode[cell.walls ^ 0b1111]
            string += tmp + '\n'
        string += '  ' * self.end[1] + 'E'
        return string

    @property
    def start_node(self):
        return self.returnCell(self.start)

    @property
    def end_node(self):
        return self.returnCell(self.end)

    def returnCell(self, pos):
        return self.grid[pos[0]][pos[1]]

    def algorithmInit(self):
        root = self.start_node
        root.knockWalls(0b1000)
        main_cell_stack = [root]
        while main_cell_stack:
            cell = random.choice(main_cell_stack)
            if cell.hasEmptyNeighbors():
                main_cell_stack += (self.algorithmShortWalk(cell))
            else:
                main_cell_stack.remove(cell)

    def algorithmShortWalk(self, root):
        max_trail = 2 * self.size // 3
        cell_stack = [root]
        while cell_stack and len(cell_stack) < max_trail:
            free_cells = cell_stack[-1].hasEmptyNeighbors()
            curr_cell = cell_stack[-1]
            if free_cells:
                if self.animate:
                    print(str(self) + '\n' + '\033[' + str(self.size +3) + 'F')
                    time.sleep(self.animate_fps)
                face, next_cell = random.choice(free_cells)
                curr_cell.knockWalls(face)
                if next_cell == self.end_node:
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

    def findSolution(self):
        solution = [self.start_node]
        self.findSolutionStep(solution)
        for cell in solution:
            cell.solution = True
        return solution

    def findSolutionStep(self, solution_stack):
        for cell in solution_stack[-1].hasOpenNeighbor():
            if cell not in solution_stack:
                if cell == self.end_node:
                    solution_stack.append(cell)
                    return True
                elif not cell.deadEnd():
                    solution_stack.append(cell)
                    if self.findSolutionStep(solution_stack):
                        return True
        solution_stack.pop()
        return False

class Cell:
    def __init__(self):
        self.walls = 0b1111
        self.neighbors = {}
        self.solution = False

    def deadEnd(self):
        count = 0
        for shift in range(4):
            if 0 == self.walls & 1 << (shift):
                count += 1
        return (count < 2)

    def setNeighbor(self, face, cell):
        if cell: self.neighbors[face] = cell

    def hasEmptyNeighbors(self):
        avaliable = []
        for face, cell in self.neighbors.items():
            if cell.isEmpty():
                avaliable.append((face, cell))
        return avaliable

    def hasOpenNeighbor(self):
        avaliable = []
        for face, cell in self.neighbors.items():
            if face & self.walls == 0:
                avaliable.append(cell)
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
    m.findSolution()
    print(m)
