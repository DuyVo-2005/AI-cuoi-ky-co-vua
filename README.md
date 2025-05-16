# Đồ án cuối kỳ nhập môn trí tuệ nhân tạo - Đề tài ứng dụng AI vào cờ vua - Nhóm 21

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

Đây là biểu đồ Success Rate (Tỷ lệ thành công) của thuật toán Q-learning theo số lượng EPISODES (số lần huấn luyện), với các giá trị khác nhau của epsilon (ε) — tham số quan trọng trong chiến lược epsilon-greedy để cân bằng giữa khám phá (explore) và khai thác (exploit).

![image](https://github.com/user-attachments/assets/0755e09b-ddea-4156-886f-cb2513234ad4)

 ![image](https://github.com/user-attachments/assets/2ac3e305-b06b-481f-9b35-cdf4156eed30)

(So sánh thời gian chạy của các thuật toán)

Nhận xét chi tiết:
-	Thuật toán Backtracking: Thời gian chạy là 0.0000 giây (làm tròn vì số rất bé) — cực kỳ nhanh. Đây là thuật toán được tối ưu rất tốt cho bài toán 8 hậu và có thể giải gần như ngay lập tức.
-	DFS (Depth-First Search): Thời gian chạy là 0.0010 giây — rất nhanh nhưng chậm hơn Backtracking một chút. DFS không đảm bảo tìm lời giải tối ưu hoặc nhanh nhất trong mọi tình huống, nhưng vẫn hoạt động hiệu quả ở đây.
-	BFS (Breadth-First Search): Thời gian chạy là 0.0120 giây — chậm hơn DFS nhiều lần. BFS cần lưu trữ nhiều trạng thái trong hàng đợi, làm tăng thời gian xử lý.
-	Q-Learning: Thời gian chạy là 0.0507 giây — cao hơn rõ rệt so với ba thuật toán trên. Q-Learning là thuật toán học tăng cường, nên mất thời gian để “học” cách giải bài toán, do đó thời gian thực thi cao hơn.
-	Partial Observation (Giả định là một phương pháp học máy với thông tin quan sát không đầy đủ): Thời gian chạy cao nhất: 0.1000 giây. Do chỉ quan sát một phần trạng thái, thuật toán này có thể cần thời gian để suy đoán phần còn lại, khiến nó tốn kém hơn.

 ![image](https://github.com/user-attachments/assets/def7d9a9-e108-464d-b059-77db16e275f0)

(So sánh không gian mở rộng của các thuật toán)

Nhận xét chi tiết:
-	Backtracking (89 trạng thái mở rộng): Thuật toán này mở rộng ít trạng thái nhất, thể hiện sự hiệu quả trong việc cắt nhánh và loại bỏ sớm các trường hợp không khả thi. Đây là lý do nó thường được sử dụng để giải bài toán 8 hậu một cách tối ưu.
-	DFS (1473 trạng thái mở rộng): DFS mở rộng nhiều trạng thái hơn so với Backtracking, bởi nó không có cơ chế cắt nhánh hiệu quả bằng. Vì vậy, thuật toán phải duyệt qua nhiều trạng thái hơn, dẫn đến chi phí tính toán cao hơn.
-	BFS (3412 trạng thái mở rộng): BFS duyệt theo từng lớp trạng thái, nên số lượng trạng thái mở rộng thường lớn hơn DFS. Điều này khiến BFS tốn nhiều bộ nhớ và thời gian hơn trong bài toán này.
-	Q-Learning (9827 trạng thái mở rộng): Thuật toán học tăng cường này phải mở rộng rất nhiều trạng thái để học được chính sách giải quyết bài toán. Do bản chất thử và sai (trial and error), nên số trạng thái mở rộng lớn hơn rất nhiều so với các thuật toán duyệt cây truyền thống.
-	Partial Observation (17654 trạng thái mở rộng): Đây là thuật toán có số trạng thái mở rộng nhiều nhất do chỉ quan sát được một phần trạng thái hiện tại, nên cần mở rộng nhiều trạng thái để bù lại phần thông tin thiếu hụt. Do đó, chi phí tính toán và bộ nhớ cũng tăng lên đáng kể.


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

![ucs_l3 mp4](https://github.com/user-attachments/assets/16a375ef-3f0b-42e3-874f-fc035cc80107)

Thuật toán IDS

![ids_l3 mp4](https://github.com/user-attachments/assets/7a42d86e-d62b-4057-a767-734c09580e1c)

Thuật toán Greedy

![greedy_l3 mp4](https://github.com/user-attachments/assets/d75b83e5-b876-49bb-804f-86c0445189c8)

Thuật toán A*

![as_l3 mp4](https://github.com/user-attachments/assets/4e065cd7-1be8-4712-95fa-75e95a7a2a9e)

Thuật toán IDA*

![ida_start_l3 mp4](https://github.com/user-attachments/assets/a177b59a-d609-42c7-9948-0700fb255a9b)

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

#### Đánh giá các thuật toán sử dụng trong trò "Vua tẩu thoát" qua biểu đồ
##### Một số hình ảnh thống kê về thời gian thực thi
![image](https://github.com/user-attachments/assets/e67799e4-4e3e-4ece-805d-5ff8172e64fe)

![image](https://github.com/user-attachments/assets/184f3e56-e3e2-41c7-afc6-d6239fddf87a)

![image](https://github.com/user-attachments/assets/7cd82bc3-289f-4ea2-aa85-28cfb8eb2507)

![image](https://github.com/user-attachments/assets/244b46f9-e11b-4441-8841-3477822ef3a9)

![image](https://github.com/user-attachments/assets/0b051fdc-a5c5-4c0a-b1c7-4114ba9d9cdc)

![image](https://github.com/user-attachments/assets/0527f835-0054-4fbc-a234-0aecb63266bc)

![image](https://github.com/user-attachments/assets/5fd539a5-822f-4a89-9a85-b28ee729f13a)

![image](https://github.com/user-attachments/assets/7a986d43-d310-4bf7-ace4-8b149ab1502e)
##### Một số hình ảnh thống kê về số bước trong lời giải
![image](https://github.com/user-attachments/assets/7f53d30a-6181-4541-8f6d-e2faffd2fabe)

![image](https://github.com/user-attachments/assets/08299615-565d-450d-9a8f-acc9052900e4)

![image](https://github.com/user-attachments/assets/db0b5628-d7a1-4639-82ee-5dcc2549f61e)

![image](https://github.com/user-attachments/assets/1f41ac1f-3ca2-4e6c-a6e2-2645d3498d87)

##### Một số hình ảnh thống kê về số không gian trạng thái mở rộng
![image](https://github.com/user-attachments/assets/08a62342-18e2-4708-a07b-519a5ffa9456)

![image](https://github.com/user-attachments/assets/0dc0b7be-adbc-4017-8435-ac14e636ea12)

![image](https://github.com/user-attachments/assets/be0d066a-dbe7-4ec1-bef8-f2336786124b)

![image](https://github.com/user-attachments/assets/99c15af1-69b7-467c-9fc8-b5ff0aca91c9)

![image](https://github.com/user-attachments/assets/37e6bc8e-9cab-4914-aec3-5b935b46d8ab)

![image](https://github.com/user-attachments/assets/98b73168-db82-466a-a501-09c449a9898f)

![image](https://github.com/user-attachments/assets/3464d9b3-89ff-48df-a1a8-6a54dcf7c760)

![image](https://github.com/user-attachments/assets/dcf6e586-095a-4871-a39a-2284b1690eca)

##### Đánh giá nhóm thuật toán tìm kiếm không có thông tin
Các thuật toán thuộc nhóm tìm kiếm không thông tin tốn nhiều thời gian thực thi do khám phá toàn bộ không gian trạng thái. BFS và IDS đặc biệt tốn thời gian do lặp lại nhiều trạng thái với trạng thái mục tiêu ở nút nhánh cây tìm kiếm (xa mức của trạng thái ban đầu do ô vua đứng ban đầu và ô cần đến ở hai biên rất xa nhau). DFS hoạt động hiệu quả do ưu tiên tìm sâu một nhánh trước khi chuyển sang nhánh khác.
Về số bước thực hiện, các thuật toán thuộc nhóm tìm kiếm không thông tin đều có số bước trong lời giải là ít nhất so với các thuật toán khác.
Về số trạng thái mở rộng, DFS và IDS tiết kiệm bộ nhớ hơn so với BFS và UCS.

##### Đánh giá nhóm thuật toán tìm kiếm có thông tin
Các thuật toán thuộc nhóm tìm kiếm có thông tin thực thi rất nhanh nhờ sử dụng hàm heuristic để định hướng, tính toán chi phí quá trình tìm kiếm. A* có thời gian thực thi trung bình rất bé vì thuật toán này tìm kiếm dựa trên chí phí ước lượng (hàm heristic) và  chi phí thực tế (g cost). IDA* có thời gian chạy trung bình lớn nhất do phải dùng A* cùng lập từng độ sâu để tìm trạng thái mục tiêu.
Về số bước thực hiện, nhóm thuật toán thuộc nhóm tìm kiếm có thông tin tìm được lời giải với số bước ở mức trung bình, trừ IDA* ở mức thấp.
Về số trạng thái mở rộng, các thuật toán nhóm này tương đương nhau ở các cấp độ trò chơi.

##### Đánh giá nhóm thuật toán tìm kiếm cục bộ
Các thuật toán thuộc nhóm thuật toán tìm kiếm cục bộ có thời gian thực thi trung bình thấp hơn so với các nhóm thuật toán khác nhưng nhóm này đa phần dễ bị mắc kẹt ở cực trị địa phương dẫn đến không tìm ra lời giải ở mức độ 4 của trò chơi. Trong nhóm này steepest ascent hill climbing (thuật toán leo đồi dốc nhất) có thời gian thực thi trung bình bé nhất do thuật toán này ưu tiên chuyển sang trạng thái có chi phí heuristic tốt nhất dẫn đến sớm tìm ra lời giải.
Về số bước thực hiện, thuật toán thuộc nhóm tìm kiếm cục bộ tìm được lời giải với số bước ở mức trung bình, trừ simple hill climbing ở mức thấp do chuyển trạng thái chỉ xét nút có chi phí tốt hơn hiện tại (không đảm bảo đó là tốt nhất).
Về số trạng thái mở rộng, Simulated Annealing tiết kiệm bộ nhớ hơn so với các thuật toán cùng nhóm. Beam search là thuật toán chiếm dụng bộ nhớ nhiều nhất trong nhóm do mỗi lần duyệt phải đưa vào và lấy ra với beam width là 2 phần tử.

##### Đánh giá nhóm thuật toán tìm kiếm trong môi trường phức tạp
Thuật toán tìm kiếm không có sự quan sát (search with no observation) có thời gian thực thi và số trạng thái mở rộng (chiếm dụng bộ nhớ) lớn hơn rất nhiều so với các nhóm thuật toán do sự phức tạp về số trạng thái ban đầu và số trạng thái mục tiêu lớn hơn so với các thuật toán khác.
Về số bước thực hiện, thuật toán tìm kiếm không có sự quan sát có số bước thực hiện trong lời giải ở mức trung bình nếu có lời giải được tìm ra.

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
