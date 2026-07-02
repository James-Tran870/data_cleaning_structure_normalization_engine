import re
import json

def load_regex_rules(config_path: str) -> list:
    """
    Đọc Sổ tay quy tắc rules.json và trích xuất các mẫu Regex.
    Nếu file cấu hình bị mất hoặc lỗi, trả về danh sách rỗng để tránh sập hệ thống.
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
            # Truy cập sâu vào cấu trúc JSON theo đúng Schema đã quy hoạch
            return config_data.get("text_refinement_pipeline", {}).get("artifact_removal_rules", [])
    except (FileNotFoundError, json.JSONDecodeError):
        # Cơ chế phòng thủ: Trả về danh sách rỗng thay vì làm sập đường ống
        return []

def apply_text_cleaning(text: str, rules: list) -> str:
    """
    LÕI 2: Quét tuần tự dòng văn bản và áp dụng các quy tắc Regex từ cấu hình.
    """
    if not text:
        return ""
        
    cleaned_text = text
    for rule in rules:
        if rule.get("enabled", False):
            pattern = rule.get("regex_pattern", "")
            replace_value = rule.get("replace_value", "")
            try:
                # Thực thi quét và thay thế chuỗi dựa trên biểu thức chính quy
                cleaned_text = re.sub(pattern, replace_value, cleaned_text, flags=re.MULTILINE)
            except re.error:
                # Nếu một mẫu biểu thức Regex bị viết sai cú pháp, bỏ qua để bảo vệ mạch chạy
                continue
                
    return cleaned_text