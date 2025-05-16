# Đồ án cuối kỳ nhập môn trí tuệ nhân tạo - Đề tài ứng dụng AI vào cờ vua

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
#### Mô tả bài toán
Không gian mô phỏng là một bàn cờ vua có kích thước 9x18, bàn cờ gồm có hai loại cờ là quân vua và quân tốt. Quân vua là quân duy nhất được di chuyển, mỗi lần di chuyển quân vua sẽ đi một ô theo một trong các hướng lên, xuống, trái, phải, chéo trên trái, chéo trên phải, chéo dưới trái hoặc chéo dưới phải. Quân tốt đóng vai trò là vật cản trong mô phỏng. Một quân tốt sẽ được đặt cố định tại một ô và quân này sẽ trấn giữ năm ô bao gồm ô nó đang đứng, ô chéo trên trái, ô chéo trên phải, ô chéo dưới trái, ô chéo dưới phải.
#### Mục tiêu của trò chơi
Áp dụng một trong các thuật toán tìm kiếm AI để tìm ra đường đi cho quân vua từ một ô đến một ô khác trên bàn cờ sao cho đường đi phải chứa các ô nằm trong bàn cờ và không được chứa các ô mà quân tốt đang trấn giữ.
#### Video chạy thử nghiệm
##### Level 1
Thuật toán BFS

![bfs_l1 mp4](https://github.com/user-attachments/assets/b403c05a-0188-43a6-8caf-8a88e2b75cc6)

Thuật toán DFS

![dfs_l1 mp4](https://github.com/user-attachments/assets/54de1a93-353d-4a33-96ff-994faeb31591)

Thuật toán UCS

![ucs_l1 mp4](https://github.com/user-attachments/assets/28ec1bf1-df86-416e-b7ae-bfa892743cbb)

Thuật toán IDS

![ids_l1 mp4](https://github.com/user-attachments/assets/ab6d1170-781b-4a27-824d-952017d9aae6)

Thuật toán Greedy

![greedy_l1 mp4](https://github.com/user-attachments/assets/48e4811f-f7be-485b-bd63-1c523ce4a0f8)

Thuật toán A*

![as_l1](https://github.com/user-attachments/assets/7df28b4a-b115-4bf1-be5f-602fd3b9f692)

Thuật toán IDA*
![idas_l1 mp4](https://github.com/user-attachments/assets/68ddf340-2b3c-4b09-9145-84546b37336b)

Thuật toán Simple hill climbing

![sim_hl_l1 mp4](https://github.com/user-attachments/assets/43b61acf-454f-4b07-82b0-862cf450fb34)

Thuật toán Steepest ascent hill climbing

![steepest_hc_l1 mp4](https://github.com/user-attachments/assets/59ec104e-bc66-4936-b7a4-ce3156c12eef)

Thuật toán stochastic hill climbing

![sto_hl_l1 mp4](https://github.com/user-attachments/assets/91bc44e7-7a2c-487f-b649-253e9c61e08c)

Thuật toán Stimulated annealing

![sa_l1 mp4](https://github.com/user-attachments/assets/eb860d25-70bb-484d-ae01-9d475159b9ef)

Thuật toán Beam Search

![beam_l1 mp4](https://github.com/user-attachments/assets/7ac78174-4d99-47cf-9254-ed4ccc4f8e80)

Thuật toán search with no observation

![search_no_ob_l1 mp4](https://github.com/user-attachments/assets/0ae23201-c944-4107-a8c1-7275cd2a972b)

##### Level 2
Thuật toán BFS

![bfs_l2 mp4](https://github.com/user-attachments/assets/ee7c7061-7545-4bac-b703-c3f453156540)

Thuật toán DFS

![dfs_l2 mp4](https://github.com/user-attachments/assets/677b95f4-eda8-4c92-91e4-ffbfb4db5cb7)

Thuật toán UCS

![ucs_l2 mp4](https://github.com/user-attachments/assets/9a89a62d-8352-4657-803d-75fba311382a)

Thuật toán IDS

![ids_l2 mp4](https://github.com/user-attachments/assets/0eefd7ce-676a-46c1-861b-4ebf9ba04636)

Thuật toán Greedy

![greedy_l2 mp4](https://github.com/user-attachments/assets/a9d2d6e7-bc89-4fc2-bb5b-8badf1d03149)

Thuật toán A*

![as_l2 mp4](https://github.com/user-attachments/assets/b060dd58-f372-4309-8c08-f484c3f4420a)

Thuật toán IDA*

![idas_l2 mp4](https://github.com/user-attachments/assets/074e818e-4236-41fe-8291-c992f528d08b)

Thuật toán Simple hill climbing

![simple_hc_l2 mp4](https://github.com/user-attachments/assets/a28f2984-0d8e-4a34-b9c4-7c9f455b567e)

Thuật toán Steepest ascent hill climbing

![steepest_ahc_l2 mp4](https://github.com/user-attachments/assets/8545a591-9b0b-47a1-a322-83bdc8b48e7f)

Thuật toán stochastic hill climbing

![stohastic_hc_l2 mp4](https://github.com/user-attachments/assets/5d5c0ce7-6c0b-42a8-8be5-860271107c56)

Thuật toán Stimulated annealing

![stimulate_annealing_l2 mp4](https://github.com/user-attachments/assets/e8b91bce-68ea-474f-a6e6-108fb98030d9)

Thuật toán Beam Search

![beam_l2 mp4](https://github.com/user-attachments/assets/090ec5b2-c909-41e3-9766-5e2e018c5fc7)

Thuật toán search with no observation

![search_no_ob_l2 mp4](https://github.com/user-attachments/assets/ee3ad115-088e-4705-9726-d701791a60ec)

##### Level 3
Thuật toán BFS

![bfs_l3 mp4](https://github.com/user-attachments/assets/56a47118-9af7-4499-82d4-f7218c5daa95)

Thuật toán DFS

![dfs_l3 mp4](https://github.com/user-attachments/assets/0d2dc5dd-e98c-45b5-80ae-a98022538003)

Thuật toán UCS

![ucs_l3](https://github.com/user-attachments/assets/d306f027-f22c-4327-8ea5-84f740bed67f)

Thuật toán IDS

![ids_l3 mp4](https://github.com/user-attachments/assets/7a42d86e-d62b-4057-a767-734c09580e1c)

Thuật toán Greedy

https://github.com/user-attachments/assets/357b2056-df78-416e-8d13-77a624e68f14

Thuật toán A*

https://github.com/user-attachments/assets/a4473fe8-bff5-46ba-bb21-ed82eeedf138

Thuật toán IDA*

https://github.com/user-attachments/assets/edf086d1-f945-4c34-b8bf-d4cc8e0da27b

Thuật toán simple hill climbing

![shc_l3 mp4](https://github.com/user-attachments/assets/68b4609b-cf98-4224-90e7-59c672e70d51)

Thuật toán Steepest ascent hill climbing

![sahc_l3 mp4](https://github.com/user-attachments/assets/d3a1d316-33d5-4a19-b984-be1f3ddd89f1)

Thuật toán stochastic hill climbing

![stochastic_hc_l3 mp4](https://github.com/user-attachments/assets/c922edff-dd09-4c64-b142-2d122ff72524)

Thuật toán Beam Search

![beam_search_l3 mp4](https://github.com/user-attachments/assets/961b8814-c6e5-4fc7-887c-25007e92ab2c)

Thuật toán search with no observation

![search_no_ob_l3 mp4](https://github.com/user-attachments/assets/00b201fe-bf91-4b27-93cb-cb60aaf94817)

##### Level 4
Thuật toán BFS

![bfs_l4 mp4](https://github.com/user-attachments/assets/b3e77bee-4741-4a16-972d-e722b96d4414)

Thuật toán DFS

![dfs_l4 mp4](https://github.com/user-attachments/assets/b8e3d00c-3a13-4855-9904-bd8d90a0668d)

Thuật toán UCS

![ucs_l4 mp4](https://github.com/user-attachments/assets/00010bfe-144c-446f-9266-4f6040d3ca6b)

Thuật toán IDS

![ids_l4 mp4](https://github.com/user-attachments/assets/955b7e48-c737-4a66-aa74-114e473468ad)

Thuật toán Greedy

![greedy_l4 mp4](https://github.com/user-attachments/assets/fc8186dc-f776-4919-a83a-5b8d11962da8)

Thuật toán A*

![as_l4 mp4](https://github.com/user-attachments/assets/d47b2849-3b60-4d1e-a34e-ed323f7bb6cb)

Thuật toán IDA*

![idas_l4 mp4](https://github.com/user-attachments/assets/9a5d9c16-ab2c-46cc-8418-5118d17f2ec2)

Thuật toán Simple hill climbing

![simple_hc_l4 mp4](https://github.com/user-attachments/assets/d1d9da55-4529-4dd4-989b-74a597faaebd)

Thuật toán Steepest ascent hill climbing

![stepest_ahc_l4 mp4](https://github.com/user-attachments/assets/affaa216-d13c-435c-b12c-f0c3478e96ec)

Thuật toán stochastic hill climbing

![stohastic_hc_l4 mp4](https://github.com/user-attachments/assets/b7b4d1bd-b2e3-4002-a0a3-c90e83e87893)

Thuật toán Stimulated annealing

![sa_l4 (1) mp4](https://github.com/user-attachments/assets/57d54976-fb7a-4709-be3b-b92d7e7a9fbb)

Thuật toán Beam Search

![beam_l4 mp4](https://github.com/user-attachments/assets/321173b8-9040-4aef-99a4-662ebe54d852)

Thuật toán search with no observation

![search_no_ob_l4 mp4](https://github.com/user-attachments/assets/c8551a57-ceca-4e2e-a226-a48843b04878)

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
