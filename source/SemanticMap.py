class SemanticCell:
    def __init__(self, id, cell_type):
        self.id = id  # ID duy nhất của cell
        self.cell_type = cell_type  # Loại cell (hành lang, giao lộ, phòng)
        self.neighbors = []  # Danh sách các cell kề cạnh

    def add_neighbor(self, neighbor):
        """Thêm cell kề cạnh nếu chưa tồn tại trong danh sách."""
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

class SemanticMap:
    def __init__(self):
        self.cells = {}  # Lưu danh sách cell ngữ nghĩa
        self.connections = []  # Lưu liên kết giữa các cell

    def load_from_file(self, file_path):
        with open(file_path, "r") as file:
            reading_obstacles = False
            reading_agents = False

            for line in file:
                tokens = line.strip().split()
                if not tokens:
                    continue

                if tokens[0] == "GridGraph":
                    self.width = int(tokens[1])  # Lưu kích thước để tham chiếu sau
                    self.height = int(tokens[2])

                elif tokens[0] == "Obstacles":
                    reading_obstacles = True
                    reading_agents = False
                    continue

                elif tokens[0] == "Agents":
                    reading_obstacles = False
                    reading_agents = True
                    continue

                if reading_obstacles:
                    obstacle_ids = [int(token) for token in tokens]

                if reading_agents:
                    agent_positions = [(int(tokens[0]), int(tokens[1]))]

        # Tạo tất cả các cell từ ID
        for cell_id in range(self.width * self.height):
            cell_type = "hallway" if cell_id not in obstacle_ids else "obstacle"
            self.cells[cell_id] = SemanticCell(cell_id, cell_type)
            print(self.cells)
    
    def get_cell_by_id(self, cell_id):
        """Trả về cell dựa vào ID nếu tồn tại, ngược lại báo lỗi."""
        if cell_id in self.cells:
            return self.cells[cell_id]
        else:
            print(f"Lỗi: Cell ID {cell_id} không tồn tại!")
            return None
