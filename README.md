# Terminal Maze Generator

## Intro

This is a basic maze generator. A more in depth creation existed before this, but sadly it was lost and recreated by memory here. This used to exist as a `curses` interactive maze.

The animation shows how the algorithm generates the initial maze then chooses where to place the start and ending points. The start point is randomly selected, however the "End" point is selected based off the longest possible solution. We wouldn't want the maze to be randomly too easy ;)

## The "algorithms"

### Building

The maze is first generated as a map of linked cells with all it's walls up. Next, a random point is selected in the first row and grows from there. Each growth cycle knocks down walls for `max_trail = 2 * self.size`. This basically helps the maze generate *longer* trails rather than a bunch of obvious dead-ends. It knocks down walls in a random direction and continues.

There is a *stack* of cells that exist only until the cell is surrounded by "neighbors".

### Solution

The algorithm to find the solution is just a recursive implementation of a [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search). The animation being shown is the *final* solution of the algorithm


# Demo

![Alt text](/resources/maze_animation.gif?raw=true "Optional Title")

# TODO

Add lost features :(

- `argparse` information such as animation fps, maze dimensions, game mode, etc.
- Add curses
    - Reimplement interactive game mode
    - Cursor on entirely visiable maze controlled by w,a,s,d
    - Cursor on invisible maze with relative view distance
