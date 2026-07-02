def forward_fill_merged_cells(row_cells: list) -> list:
    """
    Thuật toán Stateful Propagation: Điền lặp lại giá trị của ô hợp lệ liền trước.
    Chuẩn hóa chuỗi 'null' hoặc ô trống thô về khoảng trống đồng nhất trước khi xử lý.
    """
    current_value = ""
    filled_row = []
    
    for cell in row_cells:
        cleaned_cell = cell.strip()
        # Chuẩn hóa từ khóa gộp ô lỗi
        if cleaned_cell.lower() == "null":
            cleaned_cell = ""
            
        if cleaned_cell == "":
            filled_row.append(current_value if current_value != "" else "")
        else:
            current_value = cleaned_cell
            filled_row.append(current_value)
            
    return filled_row

def fix_table_geometry(lines: list) -> list:
    """
    LÕI 3: Chuẩn hóa hình học bảng biểu Markdown.
    Bảo toàn mật độ ngữ nghĩa bằng cơ chế nắn dòng và dịch chuyển ô thông minh.
    """
    fixed_lines = []
    in_table_block = False
    target_columns = 0

    for i, line in enumerate(lines):
        current_line = line.strip()
        is_separator = current_line.startswith('|') and '---' in current_line
        
        if is_separator and i > 0:
            in_table_block = True
            header_line = lines[i-1].strip()
            # Đếm số lượng cột dữ liệu thực tế của hàng tiêu đề chuẩn
            target_columns = len([c for c in header_line.split('|')[1:-1]])
            if fixed_lines:
                fixed_lines.pop()
            fixed_lines.append(header_line)

        if in_table_block:
            if not current_line.startswith('|') or current_line.count('|') <= 1:
                in_table_block = False
                fixed_lines.append(line)
                continue
                
            # 1. Phân rã toàn bộ các ô (Giữ nguyên cấu trúc hình học thô, không lọc bỏ ô trống)
            raw_cells = current_line.split('|')[1:-1]
            
            # 2. Xử lý bẫy thừa thiếu dấu '|' cục bộ ở giữa dòng bằng cách lọc bớt phần tử rỗng dư thừa ở ĐUÔI
            actual_content_cells = [c.strip() for c in raw_cells if c.strip() != ""]
            if len(raw_cells) > target_columns and len(actual_content_cells) <= target_columns:
                # Nếu số ô phân rã bị thừa do lỗi gõ dấu '|' rỗng bừa bãi, tiến hành cô lập nội dung thực
                raw_cells = [c for c in raw_cells if c.strip() != ""]
            
            # 3. Kích hoạt bộ nhớ trạng thái điền ô gộp
            filled_cells = forward_fill_merged_cells(raw_cells)
            
            # 4. Nắn chỉnh độ dài mốc chuẩn cuối cùng
            if len(filled_cells) < target_columns:
                filled_cells += [""] * (target_columns - len(filled_cells))
            elif len(filled_cells) > target_columns:
                filled_cells = filled_cells[:target_columns]
                
            # Đóng gói sản phẩm tinh khiết
            current_line = "| " + " | ".join([c.strip() for c in filled_cells]) + " |"
            fixed_lines.append(current_line)
        else:
            fixed_lines.append(line)

    return fixed_lines