import os
import json
import re
import logging
from src.filters.core_3_table import fix_table_geometry

# Cấu hình hệ thống nhật ký trực ban theo tiêu chuẩn chống lỗi
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def load_rules(config_path="config/rules.json"):
    """Nạp sổ tay quy tắc an toàn từ file JSON và kiểm tra lỗi cú pháp phòng thủ."""
    if not os.path.exists(config_path):
        logging.error(f"Không tìm thấy file cấu hình tại: {config_path}")
        return []
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            return config.get("text_refinement_pipeline", {}).get("artifact_removal_rules", [])
    except json.JSONDecodeError as e:
        logging.error(f"Tệp rules.json bị lỗi cấu hình định dạng JSON nghiêm trọng: {e}")
        return []
    except Exception as e:
        logging.error(f"Lỗi không xác định khi truy xuất sổ tay cấu hình: {e}")
        return []

def apply_text_filters(text: str, rules: list) -> str:
    """Áp dụng tuần tự các bộ lọc văn bản và ghi nhận tường minh lỗi biên dịch Regex."""
    cleaned_text = text
    for rule in rules:
        if not rule.get("enabled", False):
            continue
        try:
            pattern = rule["regex_pattern"]
            replacement = rule["replace_value"]
            # Thực thi quét chuỗi văn bản liên tục trên toàn diện tài liệu
            cleaned_text = re.sub(pattern, replacement, cleaned_text, flags=re.MULTILINE)
        except re.error as regex_err:
            # Chặn đứng lỗi nuốt ngoại lệ - Báo cáo chính xác danh tính quy tắc hỏng
            logging.error(f"Quy tắc [{rule.get('rule_id')}] ({rule.get('name')}) bị lỗi cú pháp Regex: {regex_err}")
            continue
        except Exception as e:
            logging.error(f"Lỗi hệ thống ngoài dự kiến tại quy tắc {rule.get('rule_id')}: {e}")
            continue
    return cleaned_text

def process_pipeline():
    """Điều phối dòng dữ liệu tuần tự từ bể chứa đầu vào sang đầu ra đầu ra sạch."""
    input_dir = "data/input"
    output_dir = "data/output"
    
    # Tự động khởi tạo hạ tầng lưu trữ cục bộ nếu chưa có
    os.makedirs(output_dir, exist_ok=True)
    
    rules = load_rules()
    if not rules:
        logging.warning("Danh sách quy tắc trống hoặc hỏng. Bỏ qua chu trình làm sạch văn bản.")
        
    # Quét sạch toàn bộ các tệp văn bản thô có trong bể chứa
    try:
        files = [f for f in os.listdir(input_dir) if f.endswith(('.md', '.txt'))]
    except Exception as e:
        logging.error(f"Không thể truy cập bể chứa đầu vào {input_dir}: {e}")
        return

    if not files:
        logging.warning(f"Không tìm thấy tệp tài liệu thô nào cần xử lý bên trong {input_dir}")
        return

    for filename in files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"cleaned_{filename}")
        
        logging.info(f"Hệ thống bắt đầu thu gom và làm sạch tệp tin: {filename}")
        try:
            # LÕI 1: Trạm kiểm soát mã hóa byte-level
            with open(input_path, "r", encoding="utf-8", errors="replace") as f:
                raw_content = f.read()
            
            # LÕI 2: Màng lọc xử lý chuỗi chữ thông qua cấu hình rules.json
            filtered_content = apply_text_filters(raw_content, rules)
            
            # LÕI 3: Phân rã dòng và ép hàng vào khuôn hình học bảng biểu
            raw_lines = filtered_content.splitlines()
            fixed_lines = fix_table_geometry(raw_lines)
            
            # Xuất xưởng sản phẩm tinh khiết vĩnh viễn trên ổ đĩa cục bộ
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(fixed_lines) + "\n")
                
            logging.info(f"[THÀNH CÔNG] Đã làm sạch và chuẩn hóa cấu trúc: {filename}")
        except Exception as e:
            logging.error(f"Đường ống đổ vỡ cục bộ khi đang xử lý tệp {filename}: {e}")

if __name__ == "__main__":
    process_pipeline()