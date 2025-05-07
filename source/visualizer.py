import tkinter as tk
from tkinter import Canvas
import sys
from tkinter.filedialog import askopenfilename
from CBS import HighLevelCBS
from SupportComponents import *

class Visualizer:
    def __init__(self, grid_width, grid_height, obstacles, solutions, file_path):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.obstacles = obstacles  # Danh sách các tọa độ chướng ngại vật
        self.solutions = solutions  # Danh sách các đối tượng Path

        # Tạo cửa sổ chính và canvas
        self.root = tk.Tk()
        self.root.title("Pathfinding Visualizer")
        self.canvas = Canvas(self.root, width=grid_width * 50, height=grid_height * 50, bg="white")
        self.canvas.pack()

        # Lưu các hình tròn đại diện cho agents
        self.agents_patches = []
        self.goal_patches = []
        self.initial_positions = []
        self.file_path = file_path  # Đường dẫn đến file đầu vào

    def setup_grid(self):
        """Vẽ lưới trên canvas."""
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                self.canvas.create_rectangle(y * 50, x * 50, (y + 1) * 50, (x + 1) * 50, outline="gray")

        # Vẽ chướng ngại vật
        for x, y in self.obstacles:
            self.canvas.create_rectangle(y * 50, x * 50, (y + 1) * 50, (x + 1) * 50, fill="black")

    def setup_agents_and_goals(self):
        """Khởi tạo các agent, điểm đích và vẽ đường đi trên canvas."""
        self.agents_patches.clear()
        self.goal_patches.clear()
        self.initial_positions.clear()

        colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'brown', 'gray', 'pink']
        for i, path in enumerate(self.solutions):
            color = colors[i % len(colors)]

            # Vẽ agent tại vị trí ban đầu
            start = path.Nodes[0]
            agent = self.canvas.create_oval(
                start.y * 50 + 10, start.x * 50 + 10,
                start.y * 50 + 40, start.x * 50 + 40,
                fill=color
            )
            self.agents_patches.append(agent)
            self.initial_positions.append((start.x, start.y))

            # Vẽ điểm dau
            goal = path.Nodes[0]
            x1 = goal.y * 50 + 15
            y1 = goal.x * 50 + 15
            x2 = goal.y * 50 + 35
            y2 = goal.x * 50 + 35

            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2

            k = 0.5
            x1_new = cx - (x2 - cx) * k
            y1_new = cy - (y2 - cy) * k
            x2_new = cx + (x2 - cx) * k
            y2_new = cy + (y2 - cy) * k

            self.canvas.create_rectangle(
                x1_new, y1_new, x2_new, y2_new,
                outline=color, width=2
            )

            # Vẽ điểm đích
            goal = path.Nodes[-1]
            self.canvas.create_oval(
                goal.y * 50 + 15, goal.x * 50 + 15,
                goal.y * 50 + 35, goal.x * 50 + 35,
                outline=color, width=2
            )

            # Vẽ đường đi
            for j in range(len(path.Nodes) - 1):
                start_node = path.Nodes[j]
                end_node = path.Nodes[j + 1]
                self.canvas.create_line(
                    start_node.y * 50 + 25, start_node.x * 50 + 25,
                    end_node.y * 50 + 25, end_node.x * 50 + 25,
                    fill=color, dash=(4, 4), width = 2  # Đường đứt nét
                )

    def start_animation(self):
        """Chạy hoạt ảnh cho các agent."""
        frame_per_move = 10  # Số khung hình cho mỗi bước di chuyển

        def animate(frame):
            all_done = True
            for i, path in enumerate(self.solutions):
                total_frames = (len(path.Nodes) - 1) * frame_per_move

                if frame >= total_frames:
                    # Đặt vị trí agent tại đích
                    goal_node = path.Nodes[-1]
                    self.canvas.coords(
                        self.agents_patches[i],
                        goal_node.y * 50 + 10, goal_node.x * 50 + 10,
                        goal_node.y * 50 + 40, goal_node.x * 50 + 40
                    )
                else:
                    # Tính toán nội suy để di chuyển mượt mà
                    current_segment = frame // frame_per_move
                    alpha = (frame % frame_per_move) / frame_per_move
                    start_node = path.Nodes[current_segment]
                    end_node = path.Nodes[min(current_segment + 1, len(path.Nodes) - 1)]
                    x = start_node.x + alpha * (end_node.x - start_node.x)
                    y = start_node.y + alpha * (end_node.y - start_node.y)

                    self.canvas.coords(
                        self.agents_patches[i],
                        y * 50 + 10, x * 50 + 10,
                        y * 50 + 40, x * 50 + 40
                    )
                    all_done = False

            if not all_done:
                self.root.after(50, animate, frame + 1)

        animate(0)

    def reset_map(self):
        """Reset lại bản đồ về trạng thái ban đầu."""
        for i, agent in enumerate(self.agents_patches):
            start_x, start_y = self.initial_positions[i]
            self.canvas.coords(
                agent,
                start_y * 50 + 10, start_x * 50 + 10,
                start_y * 50 + 40, start_x * 50 + 40
            )
    def close_program(self):
        self.root.destroy()
        sys.exit()

    def choose_file(self):
        """Cho phép chọn file input nhưng giữ nguyên thuật toán hiện tại."""
        file_path = askopenfilename(title="Chọn tệp đầu vào", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])

        if file_path:
            self.file_path = file_path
            print(f"Tệp được chọn: {self.file_path}")

            cbs = HighLevelCBS()
            cbs.read_input(self.file_path)
            self.solutions = cbs.run()
        
            if not self.solutions:
                print("Không tìm được giải pháp cho bài toán!")
                return

            # Cập nhật trực quan
            self.grid_width = cbs._lowLevelSolver._gridWidth
            self.grid_height = cbs._lowLevelSolver._gridHeight
            self.obstacles = [(v.x, v.y) for row in cbs._lowLevelSolver.map for v in row if v.Obstacle]

            # Làm mới canvas
            self.canvas.delete("all")
            self.setup_grid()
            self.setup_agents_and_goals()

    def visualize(self):
        """Hiển thị giao diện và các nút điều khiển."""
        self.setup_grid()
        self.setup_agents_and_goals()

        # Frame cho các nút
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        # Nút "Start"
        start_button = tk.Button(button_frame, text="Start", command=self.start_animation, bg="lightblue")
        start_button.pack(side=tk.LEFT, padx=5)

        # Nút "Reset"
        reset_button = tk.Button(button_frame, text="Reset", command=self.reset_map, bg="lightgreen")
        reset_button.pack(side=tk.LEFT, padx=5)

        # Nút "Choose File"
        choose_file_button = tk.Button(button_frame, text="Choose File", command=self.choose_file, bg="lightyellow")
        choose_file_button.pack(side=tk.LEFT, padx=5)

        # Nút "Close"
        close_button = tk.Button(button_frame, text="Close", command=self.close_program, bg="lightcoral")
        close_button.pack(side=tk.LEFT, padx=5)

        # Khởi chạy giao diện
        self.root.mainloop()
