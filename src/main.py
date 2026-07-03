# ==============================================================================
# CHỐT CHẶN MÔI TRƯỜNG: Thiết lập điểm neo hệ thống cho Runtime Sys Path
# Thêm nhãn cấu hình # noqa: E402 để báo hiệu cho Ruff bỏ qua quy tắc kiểm tra tĩnh
# ==============================================================================
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import json  # noqa: E402
import re  # noqa: E402
import logging  # noqa: E402
from src.filters.core_3_table import fix_table_geometry  # noqa: E402

# Thiết lập hệ thống nhật ký trực ban tiêu chuẩn phòng thủ
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def load_pipeline_rules(config_path: str) -> list:
    """Nạp toàn bộ các mảng quy tắc làm sạch từ rules.json và kiểm tra lỗi cú pháp."""
    if not os.path.exists(config_path):
        logging.warning(f"Không tìm thấy file cấu hình tại {config_path}. Khởi tạo danh sách trống.")
        return []
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        # Hợp nhất tất cả các tầng quy tắc văn bản và cấu trúc vào một Pipeline duy nhất
        pipeline = config.get("text_refinement_pipeline", {})
        all_rules = pipeline.get("artifact_removal_rules", []) + pipeline.get("structural_normalization_rules", [])
        return all_rules
    except json.JSONDecodeError as e:
        logging.error(f"Tệp rules.json bị lỗi định dạng JSON nghiêm trọng: {e}")
        return []
    except Exception as e:
        logging.error(f"Lỗi không xác định khi truy xuất sổ tay cấu hình: {e}")
        return []

def apply_text_filters(text: str, rules: list) -> str:
    """Áp dụng tuần tự các bộ lọc Regex động và ngăn chặn lỗi nuốt ngoại lệ âm thầm."""
    cleaned_text = text
    for rule in rules:
        if not rule.get("enabled", False):
            continue
        try:
            pattern = rule["regex_pattern"]
            replacement = rule["replace_value"]
            # Thực thi quét chuỗi văn bản liên tục toàn diện tài liệu
            cleaned_text = re.sub(pattern, replacement, cleaned_text, flags=re.MULTILINE)
        except re.error as regex_err:
            logging.error(f"Quy tắc [{rule.get('rule_id')}] ({rule.get('name')}) lỗi cú pháp Regex: {regex_err}")
            continue
    return cleaned_text

def execute_cleaning_pipeline(input_file_path: str, output_file_path: str, rules: list):
    """Điều phối luồng dữ liệu tuần tự qua liên hoàn các lõi lọc offline."""
    if not os.path.exists(input_file_path):
        logging.error(f"Không tìm thấy tệp đầu vào: {input_file_path}")
        return

    try:
        with open(input_file_path, "r", encoding="utf-8", errors="replace") as f:
            raw_content = f.read()
    except Exception as e:
        logging.error(f"Không thể đọc tệp dữ liệu: {e}")
        return

    # LÕI 2: Màng lọc Regex động xử lý toàn diện chuỗi ký tự dựa trên rules.json
    filtered_content = apply_text_filters(raw_content, rules)

    # Chuyển đổi chuỗi văn bản tổng thể thành bộ đệm dòng (giữ nguyên ký tự ngắt dòng gốc)
    lines_buffer = filtered_content.splitlines(keepends=True)

    # LÕI 3: Biên dịch cú pháp và nắn thẳng ma trận hình học bảng biểu
    final_cleaned_lines = fix_table_geometry(lines_buffer)

    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    try:
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.writelines(final_cleaned_lines)
        logging.info(f"[THÀNH CÔNG] Dữ liệu sạch toàn diện đã xuất tại: {output_file_path}")
    except Exception as e:
        logging.error(f"Lỗi ghi dữ liệu đầu ra: {e}")

if __name__ == "__main__":
    CONFIG_PATH = os.path.join(BASE_DIR, "config", "rules.json")
    INPUT_PATH = os.path.join(BASE_DIR, "data", "input", "kich_ban_loi_thuc_te.md")
    OUTPUT_PATH = os.path.join(BASE_DIR, "data", "output", "cleaned_kich_ban_loi_thuc_te.md")

    pipeline_rules = load_pipeline_rules(CONFIG_PATH)
    execute_cleaning_pipeline(INPUT_PATH, OUTPUT_PATH, pipeline_rules)