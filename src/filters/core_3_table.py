def forward_fill_merged_cells(row, vertical_states):
    """
    Xử lý ô gộp dọc dựa trên kí tự neo ngữ nghĩa (Semantic Anchor).
    Bảo toàn 100% các ô trống dữ liệu thực tế do thuộc tính rỗng.
    """
    processed_row = []
    for i, cell in enumerate(row):
        clean_cell = cell.strip()
        
        # Mỏ neo ngữ nghĩa: Chỉ kế thừa nếu ô chứa ký hiệu gộp thực sự
        if clean_cell in ["null", "^"]:
            fill_value = vertical_states[i] if i < len(vertical_states) and vertical_states[i] else ""
            processed_row.append(fill_value)
        else:
            # Bảo toàn ô trống thực tế hoặc dữ liệu gốc của hàng
            processed_row.append(cell)
            
            # Cập nhật trạng thái hàng trên cho ô kế tiếp nếu ô hiện tại có chữ
            while len(vertical_states) <= i:
                vertical_states.append("")
            if clean_cell != "":
                vertical_states[i] = cell
                
    return processed_row, vertical_states


def fix_table_geometry(lines):
    """
    Điều phối hình học cấu trúc bảng Markdown, xử lý ô gộp 2 chiều 
    và ngăn chặn hoàn toàn lỗi vòng lặp vô hạn (Infinite Loop Bug).
    """
    fixed_lines = []
    vertical_states = []
    in_table_block = False
    expected_columns = 0
    
    for current_index, line in enumerate(lines):
        clean_line = line.strip()
        
        # Phát hiện dòng phân tách cấu trúc bảng Markdown
        if clean_line.startswith('|') and "---" in clean_line:
            header_index = current_index - 1
            
            # Quét ngược tìm dòng tiêu đề bảng vật lý phía trên
            while header_index >= 0 and not lines[header_index].strip().startswith('|'):
                header_index -= 1
                
            # VAN CHẶN BIÊN DÒNG: Triệt tiêu vĩnh viễn bẫy vòng lặp vô hạn
            if header_index < 0:
                fixed_lines.append(line)
                continue
                
            in_table_block = True
            # Xác định số lượng cột tiêu chuẩn dựa trên dòng phân tách
            expected_columns = len([c for c in clean_line.split('|') if c.strip()])
            fixed_lines.append(line)
            continue
            
        # Xử lý các dòng dữ liệu nằm trong khối bảng
        if in_table_block and clean_line.startswith('|'):
            raw_cells = [c.strip() for c in line.split('|')][1:-1]
            
            # Cân bằng hình học ma trận cột (Bù hoặc cắt dấu phân cách thừa)
            if len(raw_cells) < expected_columns:
                raw_cells += [""] * (expected_columns - len(raw_cells))
            elif len(raw_cells) > expected_columns:
                raw_cells = raw_cells[:expected_columns]
                
            # Thực thi thuật toán điền ô gộp phòng thủ
            filled_cells, vertical_states = forward_fill_merged_cells(raw_cells, vertical_states)
            
            # Tái cấu trúc lại dòng văn bản Markdown hoàn chỉnh
            reconstructed_line = "| " + " | ".join(filled_cells) + " |"
            fixed_lines.append(reconstructed_line)
        else:
            # Nếu thoát khỏi khối bảng, reset lại bộ nhớ đệm trạng thái dọc
            if not clean_line.startswith('|'):
                in_table_block = False
                vertical_states = []
            fixed_lines.append(line)
            
    return fixed_lines