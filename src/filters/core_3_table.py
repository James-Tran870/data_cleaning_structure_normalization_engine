def forward_fill_merged_cells(row, vertical_states):
    """
    Xử lý ô gộp dọc và ngang dựa trên kí tự neo ngữ nghĩa (Semantic Anchor).
    Cập nhật bộ nhớ đệm liên tục để chống mất nhãn ở các hàng tiếp theo.
    """
    processed_row = []
    
    for i, cell in enumerate(row):
        clean_cell = cell.strip()
        
        while len(vertical_states) <= i:
            vertical_states.append("")
            
        if clean_cell in ["null", "^"]:
            fill_value = vertical_states[i] if vertical_states[i] else ""
            processed_row.append(fill_value)
            vertical_states[i] = fill_value
            
        elif clean_cell == "" and i == 0:
            fill_value = vertical_states[i] if vertical_states[i] else ""
            processed_row.append(fill_value)
            vertical_states[i] = fill_value
            
        else:
            processed_row.append(cell)
            if clean_cell != "":
                vertical_states[i] = cell
                
    return processed_row, vertical_states


def fix_table_geometry(lines):
    """
    Điều phối hình học cấu trúc bảng Markdown, xử lý ô gộp đa chiều,
    chống treo luồng và tự động khớp nối ký tự xuống dòng hệ thống (Dynamic Tail Match).
    """
    fixed_lines = []
    vertical_states = []
    in_table_block = False
    expected_columns = 0
    
    for current_index, line in enumerate(lines):
        # Kiểm tra xem dòng gốc đầu vào có ký tự xuống dòng hay không
        has_newline = line.endswith('\n')
        clean_line = line.strip()
        
        # Phát hiện dòng phân tách cấu trúc bảng Markdown
        if clean_line.startswith('|') and "---" in clean_line:
            header_index = current_index - 1
            while header_index >= 0 and not lines[header_index].strip().startswith('|'):
                header_index -= 1
                
            if header_index < 0:
                fixed_lines.append(clean_line + '\n' if has_newline else clean_line)
                continue
                
            in_table_block = True
            expected_columns = len([c for c in clean_line.split('|') if c.strip()])
            fixed_lines.append(clean_line + '\n' if has_newline else clean_line)
            continue
            
        # Xử lý các dòng dữ liệu nằm trong khối bảng
        if in_table_block and clean_line.startswith('|'):
            raw_cells = [c.strip() for c in line.split('|')][1:-1]
            
            if len(raw_cells) < expected_columns:
                raw_cells += [""] * (expected_columns - len(raw_cells))
            elif len(raw_cells) > expected_columns:
                standard_part = raw_cells[:expected_columns - 1]
                excess_part = " | ".join([c for c in raw_cells[expected_columns - 1:] if c.strip()])
                raw_cells = standard_part + [excess_part]
                
            filled_cells, vertical_states = forward_fill_merged_cells(raw_cells, vertical_states)
            
            # Khớp nối động đuôi \n dựa vào trạng thái dòng gốc đầu vào
            reconstructed_line = "| " + " | ".join(filled_cells) + " |"
            fixed_lines.append(reconstructed_line + '\n' if has_newline else reconstructed_line)
        else:
            if not clean_line.startswith('|'):
                in_table_block = False
                vertical_states = []
            fixed_lines.append(clean_line + '\n' if has_newline else clean_line)
            
    return fixed_lines