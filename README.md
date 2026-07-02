# Động cơ Làm sạch & Chuẩn hóa Cấu trúc Dữ liệu (Offline Engine)

Hệ thống xử lý sâu trung gian nhằm loại bỏ hoàn toàn nhiễu định dạng (số trang, dòng gãy, vỡ bảng Markdown) từ dữ liệu thô trước khi nạp vào hệ thống RAG hoặc PKM. Xử lý offline-first 100% trên máy cục bộ, bảo mật tuyệt đối dữ liệu.

## 1. Cây Cấu trúc Hệ thống Vật lý (Project Directory Tree)

Dưới đây là sơ đồ quy hoạch vị trí toàn bộ các cấu phần trong không gian làm việc. Mọi tệp tin bắt buộc phải nằm đúng phân khu để đảm bảo nguyên lý Phân tách mối quan tâm (SoC):

```text
data_cleaning_structure_normalization_engine/
├── .gitignore                     # Bộ lọc cách ly - Cách ly hoàn toàn vùng dữ liệu cá nhân input/output khỏi GitHub
├── README.md                      # Sách hướng dẫn vận hành - Tài liệu định vị và quick-start hệ thống (Bản cập nhật v1.0.0)
├── requirements.txt               # Danh sách linh kiện - Khai báo các thư viện Python xử lý offline
├── config/                        # PHÂN KHU CẤU HÌNH (Sổ tay điều khiển động)
│   └── rules.json                 # Quản lý tập trung 100% biểu thức Regex lọc nhiễu tiếng Việt (\1\2 chuẩn hóa)
├── data/                          # PHÂN KHU BỂ CHỨA DỮ LIỆU (Cách ly tuyệt đối trên máy cục bộ)
│   ├── input/                     # Nơi chứa các tệp Markdown thô cần lọc (Được bảo mật bởi .gitignore)
│   └── output/                    # Nơi xả các tệp văn bản sạch sau khi xử lý (Được bảo mật bởi .gitignore)
├── src/                           # PHÂN KHU LOGIC SẢN XUẤT (Nơi đặt máy móc cơ học)
│   ├── __init__.py                # File kỹ thuật nhận diện gói cục bộ
│   ├── main.py                    # Bộ điều phối trung tâm - Quét thư mục đầu vào và kích hoạt đường ống
│   └── filters/                   # Hệ thống 3 lõi lọc tuần tự
│       ├── __init__.py            # File kỹ thuật nhận diện gói con
│       ├── core_1_encoding.py     # LÕI 1: Trạm kiểm soát mã hóa byte-level, ép mã UTF-8 chuẩn
│       ├── core_2_text.py         # LÕI 2: Màng lọc Regex động, quét và triệt tiêu nhiễu rác chân trang
│       └── core_3_table.py        # LÕI 3: Khuôn hình học, xử lý ô gộp bằng thuật toán Stateful Propagation
└── tests/                         # PHÂN KHU PHÒNG THÍ NGHIỆM (Red-Teaming tự động)
    ├── __init__.py                # File kỹ thuật nhận diện thư mục kiểm thử
    ├── test_encoding_fixer.py     # Bài thử nghiệm áp lực bẫy chuỗi nhị phân cố ý mang tính tài liệu
    ├── test_table_fixer.py        # Bài thử nghiệm bẫy hình học bảng rỗng và thuật toán điền ô gộp
    └── test_text_cleaner.py       # Bài thử nghiệm áp lực bẫy số học ngụy trang chứa ký tự gạch đứng

```

## 2. Kiến trúc Hệ thống Đường ống 3 Lõi

* **Lõi 1 (Encoding Fixer):** Ép luồng byte thô về UTF-8 chuẩn thông qua chế độ phòng thủ `errors='replace'`, ngăn chặn 100% hiện tượng crash sập hệ thống khi gặp file lỗi.

* **Lõi 2 (Text Cleaner):** Quét biểu thức chính quy (Regex) được nạp động từ file cấu hình để xóa số trang và tự động nối liền từ tiếng Việt bị bẻ gãy do ranh giới trang vật lý.

* **Lõi 3 (Table Fixer):** Tự động khóa vùng xử lý khi phát hiện ký hiệu bảng, thực hiện dồn ô trống và điền lặp lại giá trị gộp (Forward Fill) để bảo toàn 100% mật độ thông tin ngữ nghĩa.

## 3. Sổ tay Vận hành Máy (Quick Start)

Mở Terminal tại thư mục gốc của dự án trên Windows và thực hiện tuần tự các bước sau để chạy máy:

1. Kích hoạt môi trường ảo bảo vệ cục bộ:
`.\venv\Scripts\Activate.ps1`
2. Đổ các file tài liệu thô cần làm sạch vào thư mục: `data/input/`
3. Khởi động van tổng điều phối đường ống:
`python src/main.py`
4. Nhận kết quả văn bản sạch hoàn toàn tại thư mục: `data/output/`

## 4. Nguyên lý Bảo trì Cấu hình (Tính Lũy đẳng)

Hệ thống áp dụng nguyên lý tách biệt mã nguồn và dữ liệu logic. Khi cần thêm bớt các quy tắc làm sạch văn bản, người vận hành chỉ cần chỉnh sửa các mẫu Regex tại tệp `config/rules.json`. Lưu ý ký hiệu nhóm trong file JSON bắt buộc phải viết nhân đôi dấu gạch chéo ngược thành `\\1\\2` để Python nhận diện chính xác. Trình điều phối `src/main.py` sẽ tự động cập nhật năng lực mà không cần phải can thiệp hay chỉnh sửa bất kỳ dòng mã Python nào.