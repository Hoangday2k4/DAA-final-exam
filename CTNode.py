from SupportComponents import *

# CTNode sử dụng cho CBS
class CTNode:
    def __init__(self):
        self.debugIndex = 0
        self.cost = 0
        self._constraints = []
        self._solution = []
        self._conflicts = []

    def get_solution(self) -> list:
        return self._solution

    def get_first_conflict(self):
        return self._conflicts[0]

    def add_conflict(self, new_conflict):
        self._conflicts.append(new_conflict)

    def clear_conflicts(self):
        self._conflicts.clear()

    def add_constraints(self, old_constraint_list: list, new_constraint):
        self._constraints.clear()
        for constraint in old_constraint_list:
            self._constraints.append(Constraint(constraint.Agent, constraint.Vertex, constraint.TimeStep))
        self._constraints.append(new_constraint)

    def get_constraints(self) -> list:
        return self._constraints

    def set_solution(self, new_solution: list):
        self._solution.clear()
        for path in new_solution:
            new_path = Path(path.agentIndex)
            new_path.Nodes = list(path.Nodes)

            for constraint in path.Constraints:
                new_path.Constraints.append(Constraint(constraint.Agent, constraint.Vertex, constraint.TimeStep))
            
            self._solution.append(new_path)

    def set_solution_for_agent(self, agent):
        self._solution[agent.Index] = Path(agent.Index)
        self._solution[agent.Index].Nodes = list(agent.path.Nodes)
