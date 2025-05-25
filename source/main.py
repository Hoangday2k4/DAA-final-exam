import os
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from CBS import HighLevelCBS
from visualizer import Visualizer

def select_file_via_gui():
    """Hiển thị hộp thoại chọn tệp và trả về đường dẫn tệp đã chọn."""
    Tk().withdraw()  # Ẩn cửa sổ chính của Tkinter
    file_path = askopenfilename(title="Chọn tệp đầu vào", 
                                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    return file_path

def main():
    try:
        # Chọn file input qua giao diện
        input_file = select_file_via_gui()
        if not input_file:
            print("Không có tệp nào được chọn. Kết thúc chương trình!")
            return

        print(f"Sử dụng tệp: {input_file}")

        # Khởi tạo CBS
        cbs = HighLevelCBS()
        
        # Đọc dữ liệu đầu vào từ file được chọn
        cbs.read_input(input_file)
        
        start_time = time.time()
        # Chạy thuật toán CBS
        solution = cbs.run()
        end_time = time.time()
        run_time = end_time - start_time

        if solution is None:
            print("Không tìm được giải pháp cho bài toán!")
            return
        
        print(f"Thời gian chạy: {run_time * 1000:.2f} ms")
        
        # Trích xuất thông tin để trực quan hóa
        grid_width = cbs._lowLevelSolver._gridWidth
        grid_height = cbs._lowLevelSolver._gridHeight
        obstacles = [(v.x, v.y) for row in cbs._lowLevelSolver.map for v in row if v.Obstacle]

        # Tạo và hiển thị hoạt ảnh
        visualizer = Visualizer(grid_width, grid_height, obstacles, solution, input_file)
        visualizer.visualize()
      
    except Exception as e:
        print("Không thể thực thi chương trình!")
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    main()
