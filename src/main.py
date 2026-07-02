import os

from filters.core_1_encoding import normalize_encoding, remove_ligatures
from filters.core_2_text import load_regex_rules, apply_text_cleaning
from filters.core_3_table import fix_table_geometry

def execute_pipeline(input_dir: str, output_dir: str, config_path: str):
    """
    Bộ điều phối chính: Đọc cấu hình, quét thư mục đầu vào và thực thi đường ống 3 lõi.
    """
    # Phòng thủ: Kiểm tra sự tồn tại của tệp cấu hình
    if not os.path.exists(config_path):
        print(f"[LỖI HỆ THỐNG] Không tìm thấy file cấu hình tại: {config_path}")
        return
        
    # Nạp các quy tắc Regex từ Giai đoạn 2
    rules = load_regex_rules(config_path)
    
    # Phòng thủ: Tự động tạo thư mục đầu ra nếu người dùng quên chưa tạo
    os.makedirs(output_dir, exist_ok=True)
    
    # Quét toàn bộ các tệp tin trong thư mục đầu vào
    for file_name in os.listdir(input_dir):
        if not file_name.endswith('.md') and not file_name.endswith('.txt'):
            continue  # Bỏ qua các file không thuộc định dạng văn bản chuẩn
            
        input_file_path = os.path.join(input_dir, file_name)
        output_file_path = os.path.join(output_dir, f"cleaned_{file_name}")
        
        try:
            # LÕI 1: Xử lý byte thô và lỗi mã hóa đầu vào (Đọc file dạng nhị phân)
            with open(input_file_path, 'rb') as f:
                raw_bytes = f.read()
            text_stage_1 = normalize_encoding(raw_bytes)
            text_stage_1 = remove_ligatures(text_stage_1)
            
            # LÕI 2: Áp dụng biểu thức Regex động từ rules.json
            text_stage_2 = apply_text_cleaning(text_stage_1, rules)
            
            # LÕI 3: Chuẩn hóa hình học cấu trúc bảng Markdown
            lines = text_stage_2.splitlines()
            fixed_lines = fix_table_geometry(lines)
            final_text = "\n".join(fixed_lines)
            
            # Xả dữ liệu sạch xuống ổ đĩa cục bộ
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(final_text)
                
            print(f"[THÀNH CÔNG] Đã làm sạch và chuẩn hóa cấu trúc: {file_name}")
            
        except Exception as e:
            # Cơ chế cách ly lỗi: File lỗi bị bỏ qua, hệ thống không sập, tiếp tục chạy file sau
            print(f"[CẢNH BÁO LỖI FILE] Bỏ qua file {file_name} do sự cố: {str(e)}")
            continue

if __name__ == "__main__":
    # Thiết lập đường dẫn vật lý cục bộ trong không gian dự án của bạn
    INPUT_DIRECTORY = os.path.join("data", "input")
    OUTPUT_DIRECTORY = os.path.join("data", "output")
    CONFIG_FILE = os.path.join("config", "rules.json")
    
    print("=== ĐỘNG CƠ LÀM SẠCH VÀ CHUẨN HÓA DỮ LIỆU KHỞI ĐỘNG ===")
    execute_pipeline(INPUT_DIRECTORY, OUTPUT_DIRECTORY, CONFIG_FILE)