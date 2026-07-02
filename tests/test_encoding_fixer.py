from src.filters.core_1_encoding import normalize_encoding

def test_binary_literal_whitelist_shield():
    """
    BẪY KIỂM THỬ: FR-3 Validation (Bẫy chuỗi nhị phân cố ý).
    Đảm bảo các ký tự điều khiển dạng văn bản tài liệu không bị xóa nhầm.
    """
    # 1. Giả lập đoạn text kỹ thuật chứa chuỗi literal điều khiển
    trap_text_literal = "Hướng dẫn: Chuỗi literal '\\t' biểu thị cho một khoảng Tab."
    raw_bytes = trap_text_literal.encode('utf-8')
    
    # 2. Đưa qua Trạm kiểm soát mã hóa Lõi 1
    output_text = normalize_encoding(raw_bytes)
    
    # 3. Kiểm tra áp lực: Đoạn text kỹ thuật phải giữ nguyên vẹn
    assert "\\t" in output_text, \
        "Hệ thống đã xóa nhầm chuỗi mã điều khiển mang tính tài liệu kỹ thuật!"