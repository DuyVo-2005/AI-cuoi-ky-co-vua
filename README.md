# AI-cuoi-ky-co-vua

## Nội dung
### 1. Thuật toán MiniMax và Cắt tỉa Alpha-Beta trong cờ Vua
#### Thuật toán MiniMax
##### 🎯 Mục tiêu:
Giúp máy tính tìm nước đi tốt nhất, giả sử rằng đối thủ cũng sẽ chơi một cách tối ưu.

##### 🧩 Nguyên lý hoạt động:
MiniMax tạo ra một cây trạng thái với:
Nút MAX: lượt của máy (máy muốn tối đa hóa điểm số).
Nút MIN: lượt của người chơi (máy giả định đối thủ sẽ giảm thiểu điểm số của nó).

##### 📉 Độ sâu (depth):
Do cờ vua có quá nhiều biến thể, MiniMax thường cắt ở độ sâu giới hạn, ví dụ: 3–5 lượt đi (ply) để giảm chi phí tính toán.

#### Cắt tỉa Alpha-Beta (Alpha-Beta Pruning)
##### 🎯 Mục tiêu:
Tối ưu hóa MiniMax bằng cách cắt bỏ các nhánh không cần thiết (không ảnh hưởng đến kết quả cuối cùng).

##### 📝 Giải thích:
Alpha: điểm số tốt nhất mà MAX có thể đảm bảo cho đến hiện tại.
Beta: điểm số tốt nhất mà MIN có thể đảm bảo cho đến hiện tại.

##### 📏 Nguyên tắc:
Nếu tại một nút MIN, bạn thấy giá trị nhỏ hơn Alpha, bạn có thể dừng duyệt vì MAX sẽ không bao giờ chọn nhánh đó.
Nếu tại một nút MAX, bạn thấy giá trị lớn hơn Beta, bạn cũng cắt vì MIN sẽ tránh nhánh đó.

##### 📈 Hiệu quả:
Giảm đáng kể số lượng nút phải duyệt.
Trong trường hợp lý tưởng (sắp xếp tốt), giảm độ phức tạp từ O(b^d) xuống còn O(b^(d/2)), với:
b: branching factor (số nước đi trung bình mỗi lượt),
d: độ sâu.

#### Triển khai:
Chương trình cờ vua của nhóm sử dụng thuật toán MiniMax và Cắt tỉa Alpha-Beta với độ sâu tìm kiếm là 3 (depth=3). 
Hàm đánh giá khá đơn giản, chỉ tính tổng số lượng và chất lượng của toàn bộ quân cờ trên bàn cờ.

### 2. Chạy thực nghiệm

https://github.com/user-attachments/assets/27e23564-bc2d-4694-80ec-d7b5d6b37bbd

### 3. Mini Game 8 Quân Hậu

#### Thuật toán Q-Learning

🧠 Thuật toán Q-Learning là gì?

Q-Learning là một thuật toán học tăng cường (Reinforcement Learning - RL) không mô hình (model-free), giúp một tác nhân (agent) học cách ra quyết định tối ưu trong môi trường bằng cách thử - sai và cập nhật dần dần giá trị kỳ vọng của hành động.

⚙️ Mục tiêu

Tìm ra chính sách tối ưu (optimal policy) để chọn hành động trong mỗi trạng thái sao cho tổng phần thưởng nhận được về lâu dài (cumulative reward) là lớn nhất.

📌 Nguyên lý hoạt động

Q-Learning sử dụng một bảng Q-Table với công thức cập nhật:

![image](https://github.com/user-attachments/assets/c423c175-95a2-4f10-92ad-e727263c1f90)

##### Trong đó

| Ký hiệu | Ý nghĩa |
|-------|-------|
| Q(s,a) | Giá trị Q hiện tại tại trạng thái s, hành động a |
| α | Hệ số học (learning rate) |
| r | Phần thưởng nhận được sau khi thực hiện hành động a |
| γ | Hệ số chiết khấu (discount factor), thường nằm giữa 0.9–0.99 |
| s' | Trạng thái kế tiếp |
| α' | Hành động kế tiếp (tốt nhất tại s') |

#### Tạo Q-Learning Model 

![image](https://github.com/user-attachments/assets/123b7e49-38ab-4429-95dd-c079c9088b59)

#### Giải Bài toán 8 Hậu với các Model vừa tạo

Trường hợp giải thành công với Model được Train nhiều lần:

![image](https://github.com/user-attachments/assets/52340ef3-5ce5-433b-943f-7e2aeebb523d)

Trường hợp giải thất bại với Model được Train ít:

![image](https://github.com/user-attachments/assets/88a9e4a5-619f-4ecd-b461-cb948842239b)

#### Thống kê tỉ lệ giải thành công của các Model được Train với các thông số khác nhau

![image](https://github.com/user-attachments/assets/0755e09b-ddea-4156-886f-cb2513234ad4)

Đây là biểu đồ Success Rate (Tỷ lệ thành công) của thuật toán Q-learning theo số lượng EPISODES (số lần huấn luyện), với các giá trị khác nhau của epsilon (ε) — tham số quan trọng trong chiến lược epsilon-greedy để cân bằng giữa khám phá (explore) và khai thác (exploit).

### 4. Mini Game Mã Đi Tuần

#### ♞ Mã Đi Tuần là gì?

Đây là bài toán yêu cầu tìm một hành trình của quân mã (Knight trong cờ vua) sao cho nó đi qua tất cả các ô trên bàn cờ đúng một lần duy nhất, theo luật di chuyển của quân mã.

#### 🎯 Yêu cầu bài toán

Tìm một chuỗi bước đi bắt đầu từ một ô bất kỳ.

Mỗi ô được đi đúng một lần.

Mục tiêu: đi qua tất cả N×N ô trên bàn cờ.

#### 🧠 Phân loại lời giải

| Loại tour | Mô tả |
|-------|-------|
| Open tour | Mã đi qua mọi ô một lần, không cần quay về vị trí đầu. |
| Closed tour | 	Mã đi qua mọi ô một lần và quay lại vị trí ban đầu. |

#### Video chạy thử nghiệm

https://github.com/user-attachments/assets/6b31fb3e-83c6-4ace-9667-c0945cad1297

### 5. Mini Game Vua Tẩu thoát


#### Video chạy thử nghiệm

##### Level 3
Thuật toán BFS

Thuật toán DFS

Thuật toán UCS

![ucs_l3](https://github.com/user-attachments/assets/d306f027-f22c-4327-8ea5-84f740bed67f)

Thuật toán A*

https://github.com/user-attachments/assets/a4473fe8-bff5-46ba-bb21-ed82eeedf138



## Tài liệu tham khảo 
[1].	Stuart Russell and Peter Norvig, "Russell 2020 Artificial intelligence a modern approach", xuất bản lần 4

[2].	“Các thuật toán tìm kiếm: chìa khóa mở cửa trí tuệ nhân tạo”, truy cập ngày 6 tháng 5 năm 2025 từ https://kdata.vn/tin-tuc/cac-thuat-toan-tim-kiem-chia-khoa-mo-cua-tri-tue-nhan-tao

[3].	“Thuật toán IDA*: Tìm kiếm hiệu quả” (2024 ), truy cập ngày 12 tháng 5 năm 2025 từ https://www.toolify.ai/vi/ai-news-vn/thut-ton-ida-tm-kim-hiu-qu-3083337

[4].	Brian Yu & David J. Malan (n.d), Giới thiệu về Trí tuệ nhân tạo với Python của CS50, truy cập ngày 12 tháng 5 năm 2025 từ https://cs50.harvard.edu/ai/2024/notes/3

[5].	Surajpatlcyj (2024), Sự lan truyền ràng buộc trong AI, truy cập ngày 12 tháng 5 năm 2025 từ https://www.geeksforgeeks.org/constraint-propagation-in-ai

[6].	CamelEdge (2025), Giải quyết các vấn đề thỏa mãn ràng buộc trong AI: Quay lui, nhất quán Arc và Heuristics, truy cập ngày 12 tháng 5 năm 2025 từ https://cameledge.com/post/ai/constraint-satisfaction-problems

## Thành viên
| Họ Tên | Mã số sinh viên |
|-------|-------|
| Vũ Anh Quốc | 23110296 |
| Võ Lê Khánh Duy | 23110196 |
| Phan Đình Sáng | 23110303 |

## Phân công
Quốc: main, board, dragger, bot, bot logic, minimax, bài toán quân 8 hậu.

Sáng: const, sound, theme, color, config, game, bài toán mã đi tuần.

Duy: square, piece, move, menu gui, dataStructure, bài toán vua tẩu thoát.
