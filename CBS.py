from SupportComponents import *
from LowLevel import LowLevelCBS
from HighLevel import HighLevelCBS
from CTNode import CTNode

class HighLevelCBS(HighLevelCBS):
    def __init__(self):
        self._lowLevelSolver = LowLevelCBS()
        self._agents = []
        self._open = []

    def validate_paths_in_node(self, node: CTNode) -> bool:
        valid_solution = True
        node.clear_conflicts()

        last_time_step = 0
        solution = node.get_solution()

        if not solution:
            return False

        for path in solution:
            current_node_size = len(path.Nodes)
            if last_time_step < current_node_size:
                last_time_step = current_node_size

        for i in range(last_time_step):
            for j in range(len(solution)):
                a = min(len(solution[j].Nodes) - 1, i)

                for k in range(len(solution)):
                    if j == k:
                        continue

                    b = min(len(solution[k].Nodes) - 1, i)

                    if solution[j].Nodes[a] == solution[k].Nodes[b]:
                        node.add_conflict(Conflict(
                            self._agents[solution[j].agentIndex],
                            self._agents[solution[k].agentIndex],
                            solution[j].Nodes[a],
                            i
                        ))
                        valid_solution = False
                        return valid_solution

        return valid_solution

    def find_paths_for_all_agents(self, node: CTNode) -> list[Path]:
        paths = []
        for agent in self._agents:
            start = self._lowLevelSolver.map[agent.StartStateX][agent.StartStateY]
            goal = self._lowLevelSolver.map[agent.GoalStateX][agent.GoalStateY]
            if not self._lowLevelSolver.a_star(start, goal, agent.path, node.get_constraints()):
                print(f"Không tìm thấy đường đi cho agent {agent.Index}")
                return None
            agent.path.agentIndex = agent.Index
            paths.append(agent.path)

        return paths

    
    def update_solution_by_invoking_low_level(self, node: CTNode, agent_index: int) -> bool:
        start = self._lowLevelSolver.map[self._agents[agent_index].StartStateX][self._agents[agent_index].StartStateY]
        goal = self._lowLevelSolver.map[self._agents[agent_index].GoalStateX][self._agents[agent_index].GoalStateY]

        if self._lowLevelSolver.a_star(start, goal, self._agents[agent_index].path, node.get_constraints()):
            self._agents[agent_index].path.agentIndex = agent_index
            node.set_solution_for_agent(self._agents[agent_index])
            return True
        return False
    
    '''
    def update_solution_by_invoking_low_level(self, node: CTNode, agent_index: int) -> bool:
        start = self._lowLevelSolver.map[self._agents[agent_index].StartStateX][self._agents[agent_index].StartStateY]
        goal = self._lowLevelSolver.map[self._agents[agent_index].GoalStateX][self._agents[agent_index].GoalStateY]

        # Dùng thời gian đệm nếu cần thiết để xử lý xung đột
        max_delay = 3  # Ví dụ: cho phép tác nhân chờ tối đa 3 bước
        for delay in range(max_delay + 1):
            constraints = node.get_constraints()
            new_constraints = constraints + [Constraint(self._agents[agent_index], start, delay)]
            
            if self._lowLevelSolver.a_star(start, goal, self._agents[agent_index].path, new_constraints):
                self._agents[agent_index].path.agentIndex = agent_index
                node.set_solution_for_agent(self._agents[agent_index])
                return True
        
        return False
    '''

    def run(self) -> list[Path]:
        debug_index = 0

        root = CTNode()
        root.debugIndex = debug_index
        debug_index += 1

        root.set_solution(self.find_paths_for_all_agents(root))
        root.cost = self.get_sic(root.get_solution())
        self._open.append(root)

        while self._open:
            P = self.retrieve_and_pop_node_with_lowest_cost()
            if P is None:  # Nếu không có nút nào để xử lý
                print("Không có nút khả dụng để tiếp tục!")
                break

            self.print_solution(P)

            valid = self.validate_paths_in_node(P)

            if valid:
                return P.get_solution()

            conflict = P.get_first_conflict()

            for i in range(2):
                new_ct_node = CTNode()
                new_ct_node.add_constraints(P.get_constraints(), Constraint(conflict.Agents[i], conflict.Vertex, conflict.TimeStep))
                new_ct_node.set_solution(P.get_solution())
                path_found = self.update_solution_by_invoking_low_level(new_ct_node, conflict.Agents[i].Index)

                if path_found:
                    new_ct_node.cost = self.get_sic(new_ct_node.get_solution())
                    if new_ct_node.cost < float('inf'):
                        new_ct_node.debugIndex = debug_index
                        debug_index += 1
                        self._open.append(new_ct_node)

            del P


    def print_solution(self, node: CTNode):
        solution = node.get_solution()

        for k, path in enumerate(solution):
            print(f"Agent {k}:")
            for i, row in enumerate(self._lowLevelSolver.map):
                for j, cell in enumerate(row):
                    agent_found_in_cell = False
                    for m, node in enumerate(path.Nodes):
                        if node == cell:
                            agent_found_in_cell = True
                            print(f"|{path.agentIndex},{m}| ", end="")
                            break

                    if not agent_found_in_cell:
                        if cell.Obstacle:
                            print("|_X_| ", end="")
                        else:
                            print("|___| ", end="")
                print()

    @staticmethod
    def clip(n, lower, upper):
        return max(lower, min(n, upper))

    def get_sic(self, solution: list[Path]) -> int:
        return sum(path.get_cost() for path in solution)

    def retrieve_and_pop_node_with_lowest_cost(self) -> CTNode:
        if not self._open:
            print("Không có nút nào trong _open để xử lý!")
            return None

        min_cost_index = min(range(len(self._open)), key=lambda i: self._open[i].cost)
        node = self._open.pop(min_cost_index)
        return node