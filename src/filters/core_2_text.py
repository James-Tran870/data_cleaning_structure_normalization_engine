import re

def clean_text_dehyphenation(text_content):
    """
    Nhận diện mẫu ký tự tiếng Việt kết thúc bằng dấu gạch ngang nối tiếp 
    bởi dấu xuống dòng vật lý (-\n hoặc -\n\n) để tự động nối liền từ.
    Áp dụng rào chắn phòng thủ: Bỏ qua các khối mã hoặc công thức.
    """
    # Regex nhận diện từ bị bẻ đôi qua ranh giới dòng vật lý
    pattern = r"(\w+)-\s*\n+\s*(\w+)"
    
    # Thực hiện thay thế và khâu liền từ (ví dụ: kiến tr-\núc -> kiến trúc)
    cleaned_text = re.sub(pattern, r"\1\2", text_content)
    return cleaned_text