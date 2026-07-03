from src.filters.core_3_table import fix_table_geometry, forward_fill_merged_cells

def test_empty_table_column_shield():
    """
    BẪY KIỂM THỬ: ST-001 Validation (Bẫy bảng rỗng cục bộ).
    Đảm bảo bảng bị rỗng ở giữa không bị làm lệch cấu trúc hình học của hàng.
    """
    trap_table = [
        "| Header 1 | Header 2 | Header 3 | Header 4 |",
        "| --- | --- | --- | --- |",
        "| Data 1 |  |  | Data 4 |"
    ]
    
    fixed_table = fix_table_geometry(trap_table)
    assert fixed_table[2].count('|') == fixed_table[0].count('|'), \
        "Hệ thống đã làm lệch hình học cột dữ liệu của bảng!"

def test_stateful_propagation_fill():
    """
    BẪY KIỂM THỬ: FR-2 Validation (Bẫy xử lý ô gộp).
    Đảm bảo cơ chế điền ô gộp ma trận 2 chiều tự động nhận diện và xử lý chính xác.
    """
    trap_row = ["KPI-03", "null", "99%"]
    # Khởi tạo hộc lưu trữ trạng thái dọc giả lập để tương thích với Lõi 3 mới
    mock_vertical_states = ["", "", ""]
    
    # Kích hoạt bộ truyền nhận tham số đôi và phân rã tuple đầu ra
    processed_row, updated_states = forward_fill_merged_cells(trap_row, mock_vertical_states)
    
    assert processed_row[1] == "KPI-03", \
        "Thuật toán Stateful Propagation bị mất trí nhớ, không điền được ô gộp!"