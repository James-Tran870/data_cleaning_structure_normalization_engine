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
    Đảm bảo cơ chế Forward Fill tự động điền lặp lại giá trị hợp lệ liền trước.
    """
    trap_row = ["KPI-03", "null", "99%"]
    processed_row = forward_fill_merged_cells(trap_row)
    
    assert processed_row[1] == "KPI-03", \
        "Thuật toán Stateful Propagation bị mất trí nhớ, không điền được ô gộp!"