1. Bài toán "Tìm đường đi của quân Vua (King's Tour)"
Mô tả: Quân vua trong cờ vua di chuyển 1 ô theo hướng bất kỳ. Bài toán yêu cầu tìm đường đi để quân vua di chuyển từ một ô bắt đầu đến một ô đích trên bàn cờ 8x8.
Thuật toán áp dụng:
BFS: Vì BFS tìm kiếm theo chiều rộng và đảm bảo tìm được đường đi ngắn nhất trong không gian trạng thái không có trọng số (mỗi bước di chuyển của quân Mã có chi phí như nhau). BFS sẽ duyệt qua tất cả các nước đi có thể từ vị trí ban đầu cho đến khi đến đích.
DFS: Có thể dùng để tìm một đường đi, nhưng không đảm bảo là ngắn nhất vì DFS đi sâu vào một nhánh trước khi quay lại
UCS: Nếu mỗi bước đi có chi phí khác nhau (ví dụ, tùy thuộc vào vị trí trên bàn cờ), UCS sẽ hữu ích để tìm đường đi với tổng chi phí nhỏ nhất.
...
