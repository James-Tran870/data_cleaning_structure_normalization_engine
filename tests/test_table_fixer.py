import pytest
# Nạp hàm sửa đổi hình học cấu trúc bảng ma trận từ Lõi 3
from src.filters.core_3_table import fix_table_geometry

def test_prevent_true_empty_overwrite_and_infinite_loop():
    """
    KỊCH BẢN RED-TEAMING: Xử lý triệt để bẫy ô trống thực tế và chặn đứng vòng lặp vô hạn.
    """
    
    # CASE 1: Bẫy kiểm tra ô trống dữ liệu thực tế (Chống ghi đè sai lệch)
    dirty_table_case = [
        "| Bộ Phận | Chỉ Tiêu | Ghi Chú |",
        "| --- | --- | --- |",
        "| Nhân sự | 100 | Đạt |",
        "| null | 150 | Tốt |",    # 'null' là ô gộp dọc của 'Nhân sự'
        "| Kế toán |  | Kém |"        # Cột Chỉ Tiêu trống thực tế, cấm đè số 150 vào đây
    ]
    
    expected_table_output = [
        "| Bộ Phận | Chỉ Tiêu | Ghi Chú |",
        "| --- | --- | --- |",
        "| Nhân sự | 100 | Đạt |",
        "| Nhân sự | 150 | Tốt |",    # Kế thừa thành công từ ô gộp dọc 'Nhân sự'
        "| Kế toán |  | Kém |"        # Bảo toàn ô trống thực tế (Chống lỗi Overwrite thành công)
    ]
    
    # Thực thi đối sánh hình học ma trận bảng
    assert fix_table_geometry(dirty_table_case) == expected_table_output

    # CASE 2: Bẫy kiểm tra dữ liệu mồ côi dòng đầu (Chặn đứng lỗi treo Infinite Loop)
    orphan_table_case = [
        "| --- | --- | --- |",        # Dòng phân tách mồ côi nằm ở vị trí index = 0
        "| Rác | Dữ liệu | Nhiễu |"
    ]
    
    # Đường ống phải chạy qua an toàn, không được phép treo cứng luồng xử lý CPU
    try:
        output_lines = fix_table_geometry(orphan_table_case)
        assert isinstance(output_lines, list)
    except TimeoutError:
        pytest.fail("Hệ thống bị sập do rơi vào vòng lặp vô hạn (Infinite Loop Bug)!")