from typing import List

class Vertex:
    def __init__(self, x=0, y=0, obstacle=False):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.Parent = None
        self.depth = 0
        self.Obstacle = obstacle

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Path:
    def __init__(self, agentIndex=0):
        self.agentIndex = agentIndex
        self.Nodes: List[Vertex] = []
        self.Constraints: List['Constraint'] = []

    def get_cost(self):
        # Returns the number of nodes as the cost
        return len(self.Nodes)


class Agent:
    def __init__(self, index, startStateX, startStateY, goalStateX, goalStateY):
        self.Index = index
        self.StartStateX = startStateX
        self.StartStateY = startStateY
        self.GoalStateX = goalStateX
        self.GoalStateY = goalStateY
        self.path = Path(index)


class Constraint:
    def __init__(self, agent: Agent, vertex: Vertex, timeStep: int):
        self.Agent = agent
        self.Vertex = vertex
        self.TimeStep = timeStep


class Conflict:
    def __init__(self, agent1: Agent, agent2: Agent, vertex: Vertex, timeStep: int):
        self.Agents = [agent1, agent2]
        self.Vertex = vertex
        self.TimeStep = timeStep


def Clip(n: float, lower: float, upper: float) -> float:
    return max(lower, min(n, upper))
