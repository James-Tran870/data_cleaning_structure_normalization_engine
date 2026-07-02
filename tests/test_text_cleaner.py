from src.filters.core_2_text import apply_text_cleaning

def test_math_and_statistics_shield():
    """
    BẪY KIỂM THỬ: TXT-001 Validation (Bẫy số học ngụy trang).
    Đảm bảo các chuỗi thống kê hoặc tính toán chứa dấu '|' không bị xóa nhầm.
    """
    # 1. Định nghĩa nguồn nước thử nghiệm chứa bẫy dữ liệu
    trap_input = "Doanh số quý này đạt | 1500 | sản phẩm"
    
    # 2. Định nghĩa Sổ tay quy tắc giả lập chứa luật xóa số trang (TXT-001)
    mock_rules = [
        {
            "rule_id": "TXT-001",
            "name": "standard_page_number",
            "enabled": True,
            "regex_pattern": "^\\s*.*\\s*\\|\\s*\\d+\\s*$",
            "replace_value": ""
        }
    ]
    
    # 3. Cho dòng nước chảy qua màng lọc Lõi 2
    output_text = apply_text_cleaning(trap_input, mock_rules)
    
    # 4. Kiểm tra áp lực: Đầu ra bắt buộc phải giữ nguyên trạng chuỗi gốc
    assert output_text == "Doanh số quý này đạt | 1500 | sản phẩm", \
        "Hệ thống đã bị sập bẫy số học ngụy trang và xóa mất dữ liệu cốt lõi!"