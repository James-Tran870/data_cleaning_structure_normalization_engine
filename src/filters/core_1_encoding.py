
def normalize_encoding(raw_bytes: bytes) -> str:
    """
    LÕI 1: Ép luồng byte thô về định dạng UTF-8 chuẩn.
    Áp dụng cơ chế phòng thủ chống sập hệ thống (Fault-tolerant).
    """
    if not isinstance(raw_bytes, bytes):
        # Phòng thủ: Nếu đầu vào không phải byte, ép kiểu về chuỗi văn bản an toàn
        return str(raw_bytes)
    
    try:
        # Thử biên dịch luồng byte theo chuẩn UTF-8 sạch
        return raw_bytes.decode('utf-8', errors='strict')
    except UnicodeDecodeError:
        # Cơ chế cứu cánh: Nếu phát hiện lỗi mã hóa, tự động thay thế ký tự lỗi
        # Bảo toàn mật độ thông tin và giữ hệ thống không bị crash
        return raw_bytes.decode('utf-8', errors='replace')

def remove_ligatures(text: str) -> str:
    """
    Thuật toán khử lỗi dính chữ (Ligatures) bằng từ điển ánh xạ tĩnh offline.
    """
    ligature_map = {
        "ﬁ": "fi",
        "ﬂ": "fl",
        "ﬀ": "ff",
        "ﬃ": "ffi",
        "ﬄ": "ffl"
    }
    
    cleaned_text = text
    for ligature, replacement in ligature_map.items():
        cleaned_text = cleaned_text.replace(ligature, replacement)
        
    return cleaned_text