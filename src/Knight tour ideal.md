1. Bài toán "Tìm đường đi ngắn nhất của quân Mã (Knight's Tour)"
Mô tả: Quân Mã (Knight) trong cờ vua di chuyển theo hình chữ "L". Bài toán yêu cầu tìm đường đi ngắn nhất để quân Mã di chuyển từ một ô bắt đầu đến một ô đích trên bàn cờ 8x8, hoặc tìm cách để quân Mã đi qua tất cả các ô mà không lặp lại (Knight's Tour hoàn chỉnh).
Thuật toán áp dụng:
BFS: Vì BFS tìm kiếm theo chiều rộng và đảm bảo tìm được đường đi ngắn nhất trong không gian trạng thái không có trọng số (mỗi bước di chuyển của quân Mã có chi phí như nhau). BFS sẽ duyệt qua tất cả các nước đi có thể từ vị trí ban đầu cho đến khi đến đích.
DFS: Có thể dùng để tìm một đường đi, nhưng không đảm bảo là ngắn nhất vì DFS đi sâu vào một nhánh trước khi quay lại. Nó phù hợp hơn cho bài toán Knight's Tour hoàn chỉnh (không quan tâm độ dài tối ưu).
UCS: Nếu mỗi bước đi có chi phí khác nhau (ví dụ, tùy thuộc vào vị trí trên bàn cờ), UCS sẽ hữu ích để tìm đường đi với tổng chi phí nhỏ nhất.
