def forward_fill_merged_cells(row_cells: list, vertical_states: list) -> tuple:
    """
    Thuật toán Stateful Propagation 2 chiều nâng cao.
    Thực hiện điền lặp dữ liệu ô gộp đồng thời trên cả trục ngang và trục dọc.
    """
    filled_row = []
    updated_vertical_states = list(vertical_states)
    current_horizontal_value = ""
    
    for col_idx, cell in enumerate(row_cells):
        cleaned_cell = cell.strip()
        if cleaned_cell.lower() == "null":
            cleaned_cell = ""
            
        if cleaned_cell == "":
            # 1. Ưu tiên kế thừa bộ nhớ dọc từ dòng phía trên
            if col_idx < len(updated_vertical_states) and updated_vertical_states[col_idx] != "":
                cleaned_cell = updated_vertical_states[col_idx]
            # 2. Nếu bộ nhớ dọc trống, kế thừa bộ nhớ ngang từ ô bên trái
            elif current_horizontal_value != "":
                cleaned_cell = current_horizontal_value
        else:
            # Cập nhật cả bộ nhớ dọc và bộ nhớ ngang khi có dữ liệu mới
            current_horizontal_value = cleaned_cell
            if col_idx < len(updated_vertical_states):
                updated_vertical_states[col_idx] = cleaned_cell
                
        filled_row.append(cleaned_cell if cleaned_cell != "" else " ")
        
    return filled_row, updated_vertical_states

def fix_table_geometry(lines: list) -> list:
    """
    LÕI 3: Chuẩn hóa hình học ma trận bảng Markdown 2 chiều.
    Khử hoàn toàn lỗi dịch cột, mất bộ nhớ dọc, cắt cụt dữ liệu và dòng xen kẹp.
    """
    fixed_lines = []
    in_table_block = False
    target_columns = 0
    vertical_states = []

    for i, line in enumerate(lines):
        current_line = line.strip()
        is_separator = current_line.startswith('|') and '---' in current_line
        
        # Giải quyết lỗi Phụ thuộc thứ tự dòng ngắt quãng: Quét ngược tìm Header thực sự
        if is_separator and not in_table_block:
            in_table_block = True
            header_index = i - 1
            while header_index >= 0 and not lines[header_index].strip().startswith('|'):
                header_index -= 1
                
            if header_index >= 0:
                header_line = lines[header_index].strip()
                target_columns = len([c for c in header_line.split('|')[1:-1]])
                # Khởi tạo hộc lưu trữ trạng thái dọc cố định cho các cột ma trận
                vertical_states = [""] * target_columns
                
                while len(fixed_lines) > header_index:
                    fixed_lines.pop()
                fixed_lines.append(header_line)

        if in_table_block:
            if not current_line.startswith('|') or current_line.count('|') <= 1:
                in_table_block = False
                vertical_states = []
                fixed_lines.append(line)
                continue
                
            if is_separator:
                fixed_lines.append(current_line)
                continue
                
            # Phân rã giữ nguyên vẹn cấu trúc hình học ô trống nhằm chống lỗi dịch cột
            raw_cells = current_line.split('|')[1:-1]
            
            # Cắt ngắn dữ liệu thô tạm thời để đưa vào hàm điền trạng thái tương thích số cột
            input_cells = raw_cells[:target_columns]
            if len(input_cells) < target_columns:
                input_cells += [""] * (target_columns - len(input_cells))
                
            # Kích hoạt bộ lọc trạng thái 2 chiều
            filled_cells, vertical_states = forward_fill_merged_cells(input_cells, vertical_states)
            
            # Giải quyết lỗi Cắt cụt dữ liệu: Thu gom phần đuôi dữ liệu thừa dồn vào ô cuối hàng
            if len(raw_cells) > target_columns:
                extra_content = " ".join([c.strip() for c in raw_cells[target_columns:] if c.strip()])
                if extra_content and filled_cells:
                    filled_cells[-1] = f"{filled_cells[-1]} {extra_content}".strip()
                    
            current_line = "| " + " | ".join([c.strip() for c in filled_cells]) + " |"
            fixed_lines.append(current_line)
        else:
            fixed_lines.append(line)

    # VỊ TRÍ CHUẨN HÓA CỦA PHIẾU BÀN GIAO: Đứng độc lập hoàn toàn ngoài vòng lặp for
    return fixed_lines