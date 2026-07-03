def forward_fill_merged_cells(row_cells: list, vertical_states: list) -> tuple:
    """
    Thuật toán Stateful Propagation 2 chiều nâng cao.
    Kế thừa dữ liệu ô gộp dọc/ngang dựa trên ký tự neo ngữ nghĩa (Semantic Anchor).
    Bảo toàn tuyệt đối các ô trống tự nhiên (True-Empty).
    """
    filled_row = []
    updated_vertical_states = list(vertical_states)
    current_horizontal_value = ""
    
    for col_idx, cell in enumerate(row_cells):
        cleaned_cell = cell.strip()
        if cleaned_cell.lower() == "null":
            cleaned_cell = ""
            
        # CHỐT CHẶN BẢO VỆ NGỮ NGHĨA: Chỉ kích hoạt điền lặp khi gặp Ký tự neo gộp ô thực sự
        if cleaned_cell in ["^"]:
            # Ưu tiên 1: Kế thừa bộ nhớ dọc từ hàng phía trên
            if col_idx < len(updated_vertical_states) and updated_vertical_states[col_idx] != "":
                final_value = updated_vertical_states[col_idx]
            # Ưu tiên 2: Kế thừa bộ nhớ ngang từ ô bên trái
            elif current_horizontal_value != "":
                final_value = current_horizontal_value
            else:
                final_value = ""
            
            filled_row.append(final_value)
            if col_idx < len(updated_vertical_states):
                updated_vertical_states[col_idx] = final_value
                
        # Nếu ô trống tự nhiên "", giữ nguyên trạng thái trống, ngăn chặn lỗi đè nhãn dữ liệu bừa bãi
        elif cleaned_cell == "":
            filled_row.append("")
            if col_idx < len(updated_vertical_states):
                updated_vertical_states[col_idx] = "" # Giải phóng trạng thái dọc của cột này
            current_horizontal_value = ""          # Giải phóng trạng thái ngang
            
        else:
            # Cập nhật trạng thái mới cho cả hai trục khi có dữ liệu tường minh
            filled_row.append(cleaned_cell)
            current_horizontal_value = cleaned_cell
            if col_idx < len(updated_vertical_states):
                updated_vertical_states[col_idx] = cleaned_cell
                
    return filled_row, updated_vertical_states

def fix_table_geometry(lines: list) -> list:
    """
    LÕI 3: Thiết lập khuôn hình học ma trận bảng Markdown 2 chiều.
    Triệt tiêu lỗi dịch cột, lặp vô hạn và khớp nối chính xác ký tự ngắt dòng hệ thống.
    """
    fixed_lines = []
    vertical_states = []
    in_table_block = False
    expected_columns = 0
    
    for current_index, line in enumerate(lines):
        has_newline = line.endswith('\n') or line.endswith('\r')
        # Tách biệt ký tự ngắt dòng để xử lý logic hình học thuần túy
        clean_line = line.replace('\r', '').replace('\n', '').strip()
        
        # Nhận diện dòng phân tách cấu trúc bảng Markdown
        if clean_line.startswith('|') and "---" in clean_line:
            header_index = current_index - 1
            # Quét ngược tìm dòng tiêu đề thực sự gần nhất bắt đầu bằng dấu |
            while header_index >= 0 and not lines[header_index].strip().startswith('|'):
                header_index -= 1
                
            # RÀO CHẮN CHẶN ĐỨNG VÒNG LẶP VÔ HẠN: Nếu tiêu đề mồ côi hoặc lỗi cấu trúc
            if header_index < 0:
                in_table_block = False
                fixed_lines.append(line)
                continue
                
            in_table_block = True
            # Đếm số lượng cột dựa trên hình học dấu gạch đứng chuẩn xác, không phụ thuộc chữ
            expected_columns = clean_line.count('|') - 1
            
            # Khởi tạo bộ nhớ dọc cố định theo số cột ma trận chuẩn
            vertical_states = [""] * expected_columns
            
            # Đồng bộ lại hàng tiêu đề đã nạp vào fixed_lines
            while len(fixed_lines) > header_index:
                fixed_lines.pop()
            
            cleaned_header = lines[header_index].replace('\r', '').replace('\n', '').strip()
            fixed_lines.append(cleaned_header + '\n' if has_newline else cleaned_header)
            fixed_lines.append(clean_line + '\n' if has_newline else clean_line)
            continue
            
        # Xử lý các dòng dữ liệu nằm trong khối bảng
        if in_table_block and clean_line.startswith('|'):
            raw_cells = [c.strip() for c in clean_line.split('|')][1:-1]
            
            # Khớp nối độ dài danh sách ô thô bằng mốc cột chuẩn của bảng
            if len(raw_cells) < expected_columns:
                raw_cells += [""] * (expected_columns - len(raw_cells))
            elif len(raw_cells) > expected_columns:
                standard_part = raw_cells[:expected_columns - 1]
                excess_part = " | ".join([c for c in raw_cells[expected_columns - 1:] if c.strip()])
                raw_cells = standard_part + [excess_part]
                
            # Vận hành lõi lọc trạng thái dữ liệu 2 chiều
            filled_cells, vertical_states = forward_fill_merged_cells(raw_cells, vertical_states)
            
            reconstructed_line = "| " + " | ".join(filled_cells) + " |"
            fixed_lines.append(reconstructed_line + '\n' if has_newline else reconstructed_line)
        else:
            # Thoát khối bảng khi dòng hiện tại không có ký tự bắt đầu của bảng Markdown
            if not clean_line.startswith('|'):
                in_table_block = False
                vertical_states = []
            fixed_lines.append(line)
            
    return fixed_lines