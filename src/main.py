import os
import json
from src.filters.core_2_text import clean_text_dehyphenation
from src.filters.core_3_table import fix_table_geometry

def load_pipeline_rules(config_path):
    """Nạp tệp cấu hình động rules.json phòng thủ."""
    if not os.path.exists(config_path):
        return {"global_cleaner_settings": {"enforce_utf8": True}}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"global_cleaner_settings": {"enforce_utf8": True}}

def execute_cleaning_pipeline(input_file_path, output_file_path, rules):
    """Vận hành dòng chảy dữ liệu tuần tự qua liên hoàn các lõi lọc offline."""
    if not os.path.exists(input_file_path):
        print(f"[LỖI] Không tìm thấy tệp đầu vào: {input_file_path}")
        return

    try:
        with open(input_file_path, "r", encoding="utf-8", errors="replace") as f:
            raw_content = f.read()
    except Exception as e:
        print(f"[LỖI] Không thể đọc tệp dữ liệu: {str(e)}")
        return

    # ----------------------------------------------------------------
    # LÕI 2: KHÂU LIỀN TỪ GÃY DÒNG VẬT LÝ (De-hyphenation)
    # ----------------------------------------------------------------
    text_fixed_content = clean_text_dehyphenation(raw_content)

    # Chuyển đổi chuỗi văn bản tổng thể thành các dòng độc lập để nạp vào Lõi 3
    lines_buffer = text_fixed_content.splitlines(keepends=True)

    # ----------------------------------------------------------------
    # LÕI 3: BIÊN DỊCH CÚ PHÁP & NẮN THẲNG MA TRẬN BẢNG
    # ----------------------------------------------------------------
    final_cleaned_lines = fix_table_geometry(lines_buffer)

    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    with open(output_file_path, "w", encoding="utf-8") as f:
        f.writelines(final_cleaned_lines)
    
    print(f"[THÀNH CÔNG] Dữ liệu sạch toàn diện đã xuất tại: {output_file_path}")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CONFIG_PATH = os.path.join(BASE_DIR, "config", "rules.json")
    INPUT_PATH = os.path.join(BASE_DIR, "data", "input", "kich_ban_loi_thuc_te.md")
    OUTPUT_PATH = os.path.join(BASE_DIR, "data", "output", "cleaned_kich_ban_loi_thuc_te.md")

    pipeline_rules = load_pipeline_rules(CONFIG_PATH)
    execute_cleaning_pipeline(INPUT_PATH, OUTPUT_PATH, pipeline_rules)