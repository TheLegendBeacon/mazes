from collections import defaultdict
from enum import Enum, auto
from typing import NamedTuple
from random import choice

class Wall(Enum):
    WALL = auto()
    SPACE = auto()

class Coords(NamedTuple):
    x: int
    y: int

class MazeGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = [[False for _ in range(width)] for _ in range(height)]
        self.walls =  defaultdict(lambda: Wall.WALL)
    
    # Wall getter
    def get_wall(self, point1, point2):
        return self.walls[Coords(*max(point1, point2)), Coords(*min(point1, point2))]

    # Wall setter
    def set_wall(self, point1, point2, wall: Wall):
        self.walls[Coords(*max(point1, point2)), Coords(*min(point1, point2))] = wall

    # Check if a point is valid
    def check_point_validity(self, point1):
        point = Coords(*point1)
        conditions = [0 <= point.x < self.width, 0 <= point.y < self.height]
        if sum(conditions) == 2:
            return True
        else:
            return False
    
    # Returns all valid points surrounding a given point
    def get_adjacent_points(self, point):
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        proposed_points = [(point[0]+x[0], point[1]+x[1]) for x in directions]
        valid_points = [x for x in proposed_points if self.check_point_validity(x)]
        return valid_points

    # Getter
    def __getitem__(self, index):
        return self.matrix[index[1]][index[0]]

    # Setter
    def __setitem__(self, index, visited: bool):
        self.matrix[index[1]][index[0]] = visited
    
    # Iterator
    def __iter__(self):
        for x in self.matrix:
            yield x

    def __repr__(self):
        total= str()
        total += "#"*(len(list(iter(self.matrix))[0])*2 +2)
        total += "\n"
        for y, row in enumerate(self):
            total += "#"
            for x, _ in enumerate(row):
                total += f" {['-' if self.walls[(x+1, y), (x, y)] == Wall.SPACE else ' '][-1]}"
            total += "#\n#"
            for x, _ in enumerate(row):
                total += f" {['-' if self.walls[(x, y+1), (x, y)] == Wall.SPACE else ' '][-1]}"
            total += '#\n'
        total += "#"*(len(list(iter(self.matrix))[0])*2 +2)
        return total

def maze_carver(grid: MazeGrid, coords=[Coords(0, 0)]):
    grid[coords[-1]] = True
    adjacent = [x for x in grid.get_adjacent_points(coords[-1]) if grid[x] == False]

    if len(adjacent) != 0:
        coords.append(choice(adjacent))
        grid.set_wall(coords[-1], coords[-2], Wall.SPACE)
        return maze_carver(grid, coords)
    elif len(adjacent) == 0 and len(coords) != 1:
        return maze_carver(grid, coords[:-1])
    else:
        return grid

def recursive_backtracker(width, height):
    grid = MazeGrid(width, height)
    new_grid = maze_carver(grid)
    return new_grid

if __name__ == '__main__':
    from sys import argv
    print(recursive_backtracker(int(argv[-2]), int(argv[-1])))