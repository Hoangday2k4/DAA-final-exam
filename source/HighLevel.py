from LowLevel import LowLevelCBS
from CTNode import CTNode
from SupportComponents import *

class HighLevelCBS:
    def __init__(self):
        self._lowLevelSolver = LowLevelCBS()
        self._agents = []
        self._open = []

    def run(self) -> list:
        # Placeholder for Running logic
        pass

    def get_sic(self, solution: list) -> int:
        # Placeholder for SIC logic
        pass

    def read_input(self, file_path: str):
        reading_obstacles = False
        reading_agents = False

        try:
            with open(file_path, "r") as file:
                for line in file:
                    print(line.strip())
                    if line.startswith("GridGraph"):
                        tokens = LowLevelCBS.split_string_by_whitespace(line)
                        grid_width = int(tokens[1])
                        grid_height = int(tokens[2])
                        self._lowLevelSolver.initialize_map(grid_height, grid_width)

                    elif line.strip() == "Obstacles":
                        reading_obstacles = True

                    elif line.strip() == "Agents":
                        reading_obstacles = False
                        reading_agents = True

                    elif reading_obstacles:
                        tokens = LowLevelCBS.split_string_by_whitespace(line)
                        for token in tokens:
                            index = int(token)
                            self._lowLevelSolver.map[index // self._lowLevelSolver.get_width()][index % self._lowLevelSolver.get_width()].Obstacle = True

                    elif reading_agents:
                        tokens = LowLevelCBS.split_string_by_whitespace(line)
                        start_index = int(tokens[0])
                        goal_index = int(tokens[1])
                        self._agents.append(
                            Agent(
                                len(self._agents),
                                start_index // self._lowLevelSolver.get_width(),
                                start_index % self._lowLevelSolver.get_width(),
                                goal_index // self._lowLevelSolver.get_width(),
                                goal_index % self._lowLevelSolver.get_width()
                            )
                        )
        except FileNotFoundError:
            print("Unable to open file")

    def validate_paths_in_node(self, node: CTNode) -> bool:
        # Placeholder for validation logic
        pass

    def find_paths_for_all_agents(self, node: CTNode) -> list:
        # Placeholder for pathfinding logic
        pass

    def update_solution_by_invoking_low_level(self, node: CTNode, agent_index: int) -> bool:
        # Placeholder for updating the solution
        pass

    def retrieve_and_pop_node_with_lowest_cost(self) -> CTNode:
        min_cost_index = None
        min_cost = float("inf")

        for i, ct_node in enumerate(self._open):
            if ct_node.cost < min_cost:
                min_cost = ct_node.cost
                min_cost_index = i

        if min_cost_index is not None:
            node = self._open.pop(min_cost_index)
            return node

        return None

    def print_solution(self, node: CTNode):
        # Placeholder for printing solution
        pass
