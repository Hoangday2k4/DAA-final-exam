# Multi-Agent Path Finding Using Conflict-Based Search and Structural-Semantic Topometric Maps

## Giới thiệu
Dự án này triển khai thuật toán **Conflict-Based Search (CBS)** nâng cao hơn bằng cách áp dụng **Structural-Semantic Topometric Maps** để tìm đường đi tối ưu cho nhiều tác nhân. Chương trình hỗ trợ trực quan hóa kết quả bằng giao diện `Tkinter`.

Ngôn ngữ: Python.

Thuật toán sử dụng: CBS, A*, ECBS, ...

Phương pháp: Hướng đối tượng (OOP), áp dụng bản đồ **Topometric** để giảm chi phí tính toán so với bản đồ dạng lưới truyền thống.

## Cấu trúc thư mục
```bash
your-repo/
│──[test]                                 # Các thư mục chứa file input.
│──[source]
          │── SupportComponents.py        # Định nghĩa lớp dữ liệu (Vertex, Path, Agent, Constraint).
          │── CTNode.py                   # Định nghĩa lớp lưu trữ trạng thái tìm kiếm trong cây CBS.
          │── LowLevel.py                 # Bộ giải A* cấp thấp.
          │── HighLevel.py                # Bộ giải CBS cấp cao.
          │── CBS.py                      # Cài đặt thuật toán CBS.
          │── visualizer.py               # Hiển thị và trực quan hóa đường đi.
          │── main.py                     # Chương trình chính để chạy CBS.

│── README.md                             # Tài liệu hướng dẫn sử dụng.
```

## Cách chạy chương trình
### Yêu cầu:
- Python 3.x
- Các thư viện cần thiết (`tkinter` đã có sẵn trong Python).

### Hướng dẫn chạy:
1. **Clone dự án:**
  ```bash
  git clone https://github.com/Hoangday2k4/DAA-final-exam.git
```

2. **Công cụ:**
- VS Code
- PyCharm
- Terminal
- ...

3. **Chạy chương trình:**
```bash
  python main.py
```
hoặc
```bash
  python3 main.py
```
- Bạn có thể chạy chương trình qua phần mềm hỗ trợ.

### Chú ý:
_Code vẫn đang trong quá trình debug nên vẫn còn nhiều thiếu sót._
