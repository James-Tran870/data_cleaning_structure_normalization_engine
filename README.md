# Động cơ Làm sạch & Chuẩn hóa Cấu trúc Dữ liệu (Standard Python Project)

Hệ thống xử lý sâu trung gian vận hành theo mô hình Kiến trúc Lai phân rã (Decoupled Hybrid Architecture). Động cơ chuyên đảm nhận nhiệm vụ triệt tiêu hoàn toàn nhiễu định dạng văn bản và nắn thẳng ma trận bảng biểu bán cấu trúc thô từ Repo 1 trước khi nạp vào chuỗi quản lý tri thức PKM hoặc hệ thống RAG nâng cao. Hệ thống thiết kế theo nguyên lý offline-first 100%, bảo mật tuyệt đối dữ liệu trên máy cục bộ.

## 1. Cây Cấu trúc Thư mục Vật lý (Project Directory Tree)

Sơ đồ quy hoạch không gian làm việc tuân thủ nghiêm ngặt nguyên lý Phân tách mối quan tâm (SoC), cô lập hoàn toàn giữa mã nguồn logic và dữ liệu cá nhân:

```text
data_cleaning_structure_normalization_engine/
├── .gitignore                     # Lưới lọc bảo an - Cách ly tuyệt đối dữ liệu input/output khỏi GitHub
├── README.md                      # Cẩm nang vận hành - Tài liệu hướng dẫn định vị và quản lý hệ thống
├── requirements.txt               # Danh sách linh kiện - Khai báo các thư viện Python xử lý offline
├── config/                        # PHÂN KHU CẤU HÌNH (Sổ tay tham số điều khiển động)
│   └── rules.json                 # Quản lý tập trung biểu thức Regex không tham lam và tương thích OS
├── data/                          # PHÂN KHU BỂ CHỨA DỮ LIỆU (Được cách ly bảo mật bởi .gitignore)
│   ├── input/                     # Nơi chứa tài liệu thô chứa bẫy lỗi (Hỗ trợ file .md và .txt)
│   └── output/                    # Nơi xả sản phẩm văn bản tinh khiết sau khi làm sạch cấu trúc
├── src/                           # PHÂN KHU LOGIC SẢN XUẤT (Hạ tầng mã nguồn cốt lõi)
│   ├── __init__.py                # Kỹ thuật nhận diện gói mô-đun
│   ├── main.py                    # Bộ điều phối trung tâm - Tích hợp Hộp kiểm kiểm định Validation Gates
│   └── filters/                   # Hệ thống 3 lõi lọc tuần tự
│       ├── __init__.py            # Kỹ thuật nhận diện gói con
│       ├── core_1_encoding.py     # LÕI 1: Trạm kiểm soát mã hóa byte-level, ép mã UTF-8 chuẩn phòng thủ
│       ├── core_2_text.py         # LÕI 2: Màng lọc chuỗi chữ chữ động qua cấu hình rules.json
│       └── core_3_table.py        # LÕI 3: Trạm ma trận 2 chiều, điền ô gộp bằng Stateful Propagation
└── tests/                         # PHÂN KHU PHÒNG THÍ NGHIỆM (Hạ tầng kiểm định chất lượng QA)
    ├── __init__.py                # Kỹ thuật nhận diện gói kiểm thử độc lập
    ├── test_encoding_fixer.py     # Trạm thử nghiệm lõi 1 - Bài thử bẫy chuỗi nhị phân cố ý
    ├── test_table_fixer.py        # Trạm thử nghiệm lõi 3 - Bài thử bẫy hình học bảng rỗng và ô gộp 2 chiều
    └── test_text_cleaner.py       # Trạm thử nghiệm lõi 2 - Bài thử bẫy số học ngụy trang

```

## 2. Hệ thống Cơ học 3 Lõi lọc Chuyên sâu

Dòng dữ liệu thô di chuyển qua đường ống tuần tự (Pipeline Architecture) qua 3 màng bảo vệ nghiêm ngặt:

* **Lõi 1 (Encoding Fixer):** Thực thi chế độ phòng thủ `errors='replace'` ép luồng byte lỗi về định dạng UTF-8 chuẩn, chặn đứng 100% nguy cơ crash sập đường ống.
* **Lõi 2 (Text Cleaner):** Vận hành công cụ Regex không tham lam (Non-greedy) nạp động từ cấu hình để triệt tiêu lỗi nuốt ngoại lệ, hỗ trợ linh hoạt cả hai định dạng ngắt dòng Windows (`\r\n`) và Linux (`\n`).
* **Lõi 3 (Table Fixer):** Kích hoạt thuật toán Stateful Propagation 2 chiều (Forward Fill trục dọc và trục ngang), bảo toàn cấu trúc ma trận cột, chống lỗi dịch chuyển hàng và tự động dồn nội dung tràn đuôi.

## 3. Sổ tay Vận hành và Bảo trì Hệ thống

### Kích hoạt đường ống trên máy trạm Windows

Để tránh lỗi phân giải gói cục bộ (`ModuleNotFoundError`), hệ thống bắt buộc phải được kích hoạt dưới dạng mô-đun hệ thống từ thư mục gốc của dự án theo các bước sau:

1. Mở Terminal tại thư mục gốc của dự án và kích hoạt môi trường ảo bảo vệ:
`.\venv\Scripts\Activate.ps1`
2. Đổ toàn bộ các tài liệu thô cần xử lý vào phân khu đầu vào: `data/input/`
3. Khởi động bộ điều phối trung tâm bằng lệnh chạy mô-đun:
`python -m src.main`
4. Thu nhận sản phẩm sạch tinh khiết tại phân khu đầu ra: `data/output/`

### Vận hành trạm kiểm thử tự động

Khi tiến hành thay đổi logic hoặc nâng cấp các lõi lọc, người vận hành cần chạy lệnh sau từ thư mục gốc dự án để kích hoạt toàn bộ hệ thống kiểm định QA tự động:
`pytest -v`

### Nguyên lý duy trì tính Lũy đẳng

Hệ thống thiết kế tách biệt 100% logic lập trình và biểu thức Regex. Mọi hành vi điều chỉnh quy tắc khử nhiễu tiếng Việt chỉ được thực hiện tại tệp `config/rules.json`. Khi khai báo mẫu tìm kiếm trong file JSON, các ký hiệu backreference bắt buộc phải nhân đôi dấu gạch chéo ngược thành `\\1\\2` để trình điều phối phân giải chính xác sang mã Python.

## 4. Chính sách Bảo mật Kho lưu trữ (Git Security Policy)

Hệ thống thiết lập hàng rào bảo an nghiêm ngặt nhằm chống rò rỉ tri thức cá nhân lên mạng công cộng:

* Toàn bộ nội dung nằm trong `data/input/` và `data/output/` bị chặn vĩnh viễn bởi `.gitignore`.
* Lịch sử theo dõi của Git (Git Index) đối với hai phân khu này đã được gỡ bỏ hoàn toàn bằng lệnh `--cached` để đảm bảo tính an toàn tuyệt đối khi thực hiện lệnh đẩy mã nguồn `git push`.