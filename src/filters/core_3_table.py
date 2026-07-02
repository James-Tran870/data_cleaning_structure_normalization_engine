def fix_table_geometry(lines: list) -> list:
    """
    LÕI 3: Chuẩn hóa hình học bảng biểu Markdown.
    Bảo toàn mật độ ngữ nghĩa bằng thuật toán dồn ô trống thông minh.
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
            # Số cột chuẩn = số lượng ô dữ liệu giữa các dấu '|'
            target_columns = len([c for c in header_line.split('|')[1:-1]])
            if fixed_lines:
                fixed_lines.pop()
            fixed_lines.append(header_line)

        if in_table_block:
            if not current_line.startswith('|') or current_line.count('|') <= 1:
                in_table_block = False
                fixed_lines.append(line)
                continue
                
            # Phân rã các ô dữ liệu thực tế bên trong dòng
            raw_cells = current_line.split('|')[1:-1]
            # Thuật toán thông minh: Lọc bỏ các ô trống bừa bãi sinh ra do lỗi gộp ô của Repo 1
            valid_cells = [c.strip() for c in raw_cells if c.strip() != ""]
            
            # Điều nắn kích thước hòm đồ về đúng kích thước mốc chuẩn
            if len(valid_cells) < target_columns:
                # Nếu thiếu ô dữ liệu, bù các ô trống vào cuối
                valid_cells += [""] * (target_columns - len(valid_cells))
            elif len(valid_cells) > target_columns:
                # Nếu thừa, chỉ cắt bỏ các phần tử trống thực sự ở đuôi
                valid_cells = valid_cells[:target_columns]
                
            # Đóng gói lại hàng Markdown hoàn chỉnh
            current_line = "| " + " | ".join(valid_cells) + " |"
            fixed_lines.append(current_line)
        else:
            fixed_lines.append(line)

    return fixed_lines