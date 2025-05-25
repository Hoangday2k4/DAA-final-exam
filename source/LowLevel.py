from SupportComponents import *

class LowLevelCBS:
    def __init__(self):
        self._gridWidth = 0
        self._gridHeight = 0
        self.map = []
        self._open = []
        self._closed = []
    
    def get_width(self):
        return self._gridWidth

    def initialize_map(self, height: int, width: int):
        self._gridHeight = height
        self._gridWidth = width
        self.map = [[Vertex(i, j) for j in range(width)] for i in range(height)]

    @staticmethod
    def split_string_by_whitespace(string: str):
        return string.split()

    def a_star(self, start: Vertex, goal: Vertex, path: Path, constraints: list[Constraint]) -> bool:
        self.clear_map_a_star_values()
        start.g = 0
        start.f = self.heuristic_cost_estimate(start, goal)
        start.depth = 0
        self.init_open_and_closed(start)

        while self._open and len(self._closed) < self._gridHeight * self._gridWidth * 20:
            current = min(self._open, key=lambda v: v.f)
            self._open.remove(current)

            if current == goal:
                path.Nodes = self.reconstruct_path(current)
                return True

            successors = []
            self.fill_neighbors(current, successors)

            for successor in successors:
                if successor in self._closed:
                    continue

                new_cost = current.g + self.heuristic_cost_estimate(successor, current)

                if successor not in self._open and not self.has_conflict(successor, current.depth + 1, constraints):
                    self._open.append(successor)
                elif new_cost >= successor.g:
                    continue

                if not self.has_conflict(successor, current.depth + 1, constraints):
                    successor.Parent = current
                    successor.depth = current.depth + 1
                    successor.g = new_cost
                    successor.f = successor.g + self.heuristic_cost_estimate(successor, goal)

            self._closed.append(current)

        return False

    def clear_map_a_star_values(self):
        for row in self.map:
            for vertex in row:
                vertex.g = 0
                vertex.h = 0
                vertex.f = 0
                vertex.depth = 0
                vertex.Parent = None

    def init_open_and_closed(self, start: Vertex):
        self._open = [start]
        self._closed = []

    def fill_neighbors(self, node: Vertex, successors: list[Vertex]):
        neighbor_offsets = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        for dx, dy in neighbor_offsets:
            nx, ny = node.x + dx, node.y + dy
            if 0 <= nx < self._gridHeight and 0 <= ny < self._gridWidth:
                neighbor = self.map[nx][ny]
                if not neighbor.Obstacle:
                    successors.append(neighbor)

    @staticmethod
    def heuristic_cost_estimate(a: Vertex, b: Vertex) -> int:
        return abs(a.x - b.x) + abs(a.y - b.y)

    @staticmethod
    def reconstruct_path(node: Vertex) -> list[Vertex]:
        path = []
        while node:
            path.append(node)
            node = node.Parent
        return list(reversed(path))
    '''
    @staticmethod
    def has_conflict(vertex: Vertex, time: int, constraints: list[Constraint]) -> bool:
        return any(c.TimeStep == time and c.Vertex == vertex for c in constraints)
    
    '''
    @staticmethod
    def has_conflict(vertex: Vertex, time: int, constraints: list[Constraint]) -> bool:
        # Kiểm tra xung đột vị trí
        if any(c.TimeStep == time and c.Vertex == vertex for c in constraints):
            return True

        # Kiểm tra xung đột cạnh bằng cách theo dõi di chuyển hai chiều
        for constraint in constraints:
            if constraint.TimeStep == time - 1:
                prev_vertex = constraint.Vertex
                if prev_vertex and vertex:
                    if (prev_vertex.x == vertex.x and prev_vertex.y == vertex.y) or \
                    (prev_vertex.x == vertex.y and prev_vertex.y == vertex.x) or \
                    (prev_vertex.x == vertex.x and prev_vertex.y == vertex.y and 
                    constraint.Agent != vertex.Agent):  # Kiểm tra cùng di chuyển trên cùng cạnh
                        return True

        return False
    #'''