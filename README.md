# AI-cuoi-ky-co-vua

## Nội dung
### 1. Thuật toán MiniMax và Cắt tỉa Alpha-Beta trong cờ Vua
#### Thuật toán MiniMax
🎯 Mục tiêu:
Giúp máy tính tìm nước đi tốt nhất, giả sử rằng đối thủ cũng sẽ chơi một cách tối ưu.

🧩 Nguyên lý hoạt động:
MiniMax tạo ra một cây trạng thái với:
Nút MAX: lượt của máy (máy muốn tối đa hóa điểm số).
Nút MIN: lượt của người chơi (máy giả định đối thủ sẽ giảm thiểu điểm số của nó).

📉 Độ sâu (depth):
Do cờ vua có quá nhiều biến thể, MiniMax thường cắt ở độ sâu giới hạn, ví dụ: 3–5 lượt đi (ply) để giảm chi phí tính toán.
#### Cắt tỉa Alpha-Beta (Alpha-Beta Pruning)
🎯 Mục tiêu:
Tối ưu hóa MiniMax bằng cách cắt bỏ các nhánh không cần thiết (không ảnh hưởng đến kết quả cuối cùng).

📝 Giải thích:
Alpha: điểm số tốt nhất mà MAX có thể đảm bảo cho đến hiện tại.
Beta: điểm số tốt nhất mà MIN có thể đảm bảo cho đến hiện tại.

📏 Nguyên tắc:
Nếu tại một nút MIN, bạn thấy giá trị nhỏ hơn Alpha, bạn có thể dừng duyệt vì MAX sẽ không bao giờ chọn nhánh đó.
Nếu tại một nút MAX, bạn thấy giá trị lớn hơn Beta, bạn cũng cắt vì MIN sẽ tránh nhánh đó.

📈 Hiệu quả:
Giảm đáng kể số lượng nút phải duyệt.
Trong trường hợp lý tưởng (sắp xếp tốt), giảm độ phức tạp từ O(b^d) xuống còn O(b^(d/2)), với:
b: branching factor (số nước đi trung bình mỗi lượt),
d: độ sâu.

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
