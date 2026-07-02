from src.filters.core_3_table import fix_table_geometry

def test_empty_table_column_shield():
    """
    BẪY KIỂM THỬ: ST-001 Validation (Bẫy bảng rỗng cục bộ).
    Đảm bảo bảng bị rỗng ở giữa không bị làm lệch cấu trúc hình học của hàng.
    """
    # 1. Giả lập một bảng Markdown bị trống 2 cột ở giữa
    trap_table = [
        "| Header 1 | Header 2 | Header 3 | Header 4 |",
        "| --- | --- | --- | --- |",
        "| Data 1 |  |  | Data 4 |"
    ]
    
    # 2. Đưa qua màng lọc nắn chỉnh hình học Lõi 3
    fixed_table = fix_table_geometry(trap_table)
    
    # 3. Kiểm tra áp lực: Số lượng cột (dấu '|') ở hàng dữ liệu phải giữ đúng bằng hàng tiêu đề (5 dấu '|')
    assert fixed_table[2].count('|') == fixed_table[0].count('|'), \
        "Hệ thống đã làm lệch hình học cột dữ liệu của bảng!"