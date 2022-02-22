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
        self.end = None
        self.grid = []
        self.size = size
        self.start = None

    def __str__(self):
        return self.gridToStr(self.grid)

    @property
    def formatted(self):
        return self.formattedStr(self.grid)

    @property
    def solution(self):
        return self.formattedStr(self.grid, view_solution=True)

    @property
    def start_node(self):
        return self.grid[self.start[0]][self.start[1]]

    @property
    def end_node(self):
        return self.grid[self.end[0]][self.end[1]]

    def algorithmInit(self):
        main_cell_stack = [random.choice(self.grid[0])]
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
                    print(str(self) + '\n' + '\033[' + str(self.size + 3) + 'F')
                    time.sleep(self.animate_fps)
                face, next_cell = random.choice(free_cells)
                curr_cell.knockWalls(face)
                cell_stack.append(next_cell)
            else:
                cell_stack.pop()
        return cell_stack

    def findLongestSolution(self):
        longest = []
        for x in range(0, self.size - 1, 2):
            self.end = (self.size - 1, x)
            longest = max(self.findSolution(), longest, key=len)
        for cell in longest:
            cell.solution = True
        self.setEndCell(self.grid[-1].index(longest[-1]))

    def findSolution(self):
        solution = [self.start_node]
        self.findSolutionStep(solution)
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

    def generateBlank(self, grid):
        for y in range(self.size):
            tmp = []
            for x in range(self.size):
                tmp.append(Cell())
            grid.append(tmp)

    def generateMaze(self):
        self.grid = []
        self.generateBlank(self.grid)
        self.linkCells(self.grid, self.size)
        self.algorithmInit()
        self.setStartCell()
        self.findLongestSolution()

    def formattedStr(self, grid, view_solution=False):
        string = '  ' # Gives a little space from edge of terminal
        string += '  ' * self.start[1] + 'S ' + '  ' * (self.size - self.start[1] - 1)
        for row in grid:
            tmp = '\n  ' # Same extra space
            for cell in row:
                if cell.solution and view_solution:
                    tmp += '\033[34m' + gui_encode[cell.walls ^ 0b1111] + '\033[0m'
                else:
                    tmp += gui_encode[cell.walls ^ 0b1111]
            string += tmp
        string += '\n  ' + '  ' * self.end[1] + 'E ' + '  ' * (self.size - self.end[1] - 1)
        return string


    def gridToStr(self, grid):
        string = ''
        for row in grid:
            tmp = '  ' # Give a little space from edge of terminal
            for cell in row:
                 tmp += gui_encode[cell.walls ^ 0b1111]
            string += tmp + '\n'
        return string

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

    def run(self):
        self.generateMaze()
        self.findLongestSolution()

    def setEndCell(self, x_pos=None):
        if x_pos:
            self.end = (size - 1, x_pos)
        else:
            self.end = (self.size - 1, random.randint(0, self.size - 1))
        self.end_node.knockWalls(0b0100)

    def setStartCell(self):
        self.start = (0, random.randint(0, self.size - 1))
        self.start_node.knockWalls(0b1000)

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


def simulateLongestSolution(maze):
    for row in maze.grid:
        for cell in row:
            cell.solution = False
    for x in range(0, maze.size, 2):
        maze.end = (maze.size - 1, x)
        maze.end_node.knockWalls(0b0100)
        solution = maze.findSolution()
        for cell in solution:
            cell.solution = True
        print(str(maze.solution) + '\033[' + str(maze.size + 2) + 'F')
        maze.end_node.walls |= 0b0100
        for cell in solution:
            cell.solution = False
        time.sleep(4 / maze.size)
    maze.findLongestSolution()
    print(maze.solution)
    time.sleep(0.5)


if __name__ == '__main__':
    size = 10
    animate_fps = 0.005
    try:
        size = int(sys.argv[1])
        animate_fps = float(sys.argv[2])
    except IndexError: pass
    m = Maze(size, animate_fps)
    try: m.run()
    except KeyboardInterrupt: pass
    simulateLongestSolution(m)
