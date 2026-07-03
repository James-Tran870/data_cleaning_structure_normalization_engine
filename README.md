# Động cơ Làm sạch & Chuẩn hóa Cấu trúc Dữ liệu (Standard Python Project)

Hệ thống xử lý sâu trung gian vận hành theo mô hình Kiến trúc Lai phân rã (Decoupled Hybrid Architecture). Động cơ chuyên đảm nhận nhiệm vụ triệt tiêu hoàn toàn nhiễu định dạng văn bản và nắn thẳng ma trận bảng biểu bán cấu trúc thô từ Repo 1 trước khi nạp vào chuỗi quản lý tri thức PKM hoặc hệ thống RAG nâng cao. Hệ thống được thiết kế theo nguyên lý offline-first 100%, bảo mật tuyệt đối dữ liệu trên máy cục bộ.

---

## 1. Cây Cấu trúc Thư mục Vật lý (Project Directory Tree)

Sơ đồ quy hoạch không gian làm việc tuân thủ nghiêm ngặt nguyên lý Phân tách mối quan tâm (SoC), cô lập hoàn toàn giữa mã nguồn logic, cấu hình hệ thống và dữ liệu cá nhân:

```text
data_cleaning_structure_normalization_engine/
├── .gitignore                     # Lưới lọc bảo an - Cách ly tuyệt đối dữ liệu input/output khỏi GitHub[cite: 2]
├── README.md                      # Cẩm nang vận hành - Tài liệu hướng dẫn định vị và quản lý hệ thống[cite: 2]
├── requirements.txt               # Danh sách linh kiện - Khai báo các thư viện Python xử lý offline[cite: 2]
├── .pytest_cache/                 # Thư mục đệm hệ thống tự động sinh ra khi chạy bộ kiểm thử pytest[cite: 2]
├── venv/                          # Môi trường ảo Python độc lập để cô lập các gói thư viện cục bộ[cite: 2]
├── config/                        # PHÂN KHU CẤU HÌNH (Sổ tay tham số điều khiển động)[cite: 2]
│   └── rules.json                 # Quản lý tập trung biểu thức Regex không tham lam và tương thích OS[cite: 2]
├── data/                          # PHÂN KHU BỂ CHỨA DỮ LIỆU (Được cách ly bảo mật bởi .gitignore)[cite: 2]
│   ├── input/                     # Nơi chứa tài liệu thô chứa bẫy lỗi (Hỗ trợ file .md và .txt)[cite: 2]
│   │   ├── .gitkeep               # File neo giữ cấu trúc thư mục rỗng khi đồng bộ Git[cite: 2]
│   │   └── kich_ban_loi_thuc_te.md # File dữ liệu thô đầu vào chứa các bẫy nhiễu cấu trúc[cite: 2]
│   └── output/                    # Nơi xả sản phẩm văn bản tinh khiết sau khi làm sạch cấu trúc[cite: 2]
│       ├── .gitkeep               # File neo giữ cấu trúc thư mục rỗng khi đồng bộ Git[cite: 2]
│       └── cleaned_kich_ban_loi_thuc_te.md # Sản phẩm tri thức sạch toàn diện xuất bản từ đường ống[cite: 2]
├── src/                           # PHÂN KHU LOGIC SẢN XUẤT (Hạ tầng mã nguồn cốt lõi)[cite: 2]
│   ├── __init__.py                # Kỹ thuật nhận diện gói mô-đun cấp cao[cite: 2]
│   ├── main.py                    # Bộ điều phối trung tâm - Tích hợp Hộp kiểm kiểm định Validation Gates[cite: 2]
│   ├── __pycache__/               # Bộ nhớ đệm biên dịch mã máy tạm thời của phân khu nguồn[cite: 2]
│   └── filters/                   # Hệ thống 3 lõi lọc tuần tự biệt lập[cite: 2]
│       ├── __init__.py            # Kỹ thuật nhận diện gói con[cite: 2]
│       ├── __pycache__/           # Bộ nhớ đệm biên dịch mã máy tạm thời của phân khu lõi lọc[cite: 2]
│       ├── core_1_encoding.py     # LÕI 1: Trạm kiểm soát mã hóa byte-level, ép mã UTF-8 chuẩn phòng thủ[cite: 2]
│       ├── core_2_text.py         # LÕI 2: Màng lọc chuỗi chữ động khâu liền từ ngữ bị gãy dòng vật lý[cite: 2]
│       └── core_3_table.py        # LÕI 3: Trạm ma trận 2 chiều, điền ô gộp bằng Stateful Propagation[cite: 2]
└── tests/                         # PHÂN KHU PHÒNG THÍ NGHIỆM (Hạ tầng kiểm định chất lượng QA)[cite: 2]
    ├── __init__.py                # Kỹ thuật nhận diện gói kiểm thử độc lập[cite: 2]
    ├── __pycache__/               # Bộ nhớ đệm biên dịch mã máy tạm thời của phân khu kiểm thử[cite: 2]
    ├── test_encoding_fixer.py     # Trạm thử nghiệm lõi 1 - Bài thử bẫy chuỗi nhị phân cố ý[cite: 2]
    ├── test_table_fixer.py        # Trạm thử nghiệm lõi 3 - Bài thử bẫy hình học bảng rỗng và ô gộp 2 chiều[cite: 2]
    └── test_text_cleaner.py       # Trạm thử nghiệm lõi 2 - Bài thử bẫy số học ngụy trang[cite: 2]

```

---

## 2. Hệ thống Cơ học 3 Lõi lọc Chuyên sâu

Dòng dữ liệu thô di chuyển qua đường ống tuần tự (Pipeline Architecture) qua 3 màng bảo vệ nghiêm ngặt:

* **Lõi 1 (Encoding Fixer):** Thực thi chế độ phòng thủ `errors='replace'` ép luồng byte lỗi về định dạng UTF-8 chuẩn, chặn đứng 100% nguy cơ sập đường ống khi gặp mã độc hoặc ký tự lạ.

* **Lõi 2 (Text Cleaner):** Vận hành công cụ Regex không tham lam (Non-greedy) nạp động từ cấu hình để triệt tiêu lỗi nuốt ngoại lệ, hỗ trợ linh hoạt cả hai định dạng ngắt dòng Windows (`\r\n`) và Linux (`\n`).

* **Lõi 3 (Table Fixer):** Kích hoạt thuật toán Stateful Propagation 2 chiều (Forward Fill trục dọc và trục ngang), bảo toàn cấu trúc ma trận cột, chống lỗi dịch chuyển hàng và tự động dồn nội dung tràn đuôi bằng cơ chế Dynamic Tail Match.

---

## 3. Sổ tay Vận hành và Bảo trì Hệ thống

### Kích hoạt đường ống trên máy trạm Windows

Để tránh lỗi phân giải gói cục bộ (`ModuleNotFoundError`), hệ thống bắt buộc phải được kích hoạt dưới dạng mô-đun hệ thống từ thư mục gốc của dự án theo các bước sau:

* **Bước 1:** Mở Terminal tại thư mục gốc của dự án và kích hoạt môi trường ảo bảo vệ:
`.\venv\Scripts\Activate.ps1`

* **Bước 2:** Đổ toàn bộ các tài liệu thô cần xử lý vào phân khu đầu vào:
`data/input/`

* **Bước 3:** Khởi động bộ điều phối trung tâm bằng lệnh chạy mô-đun:
`python -m src.main`

* **Bước 4:** Thu nhận sản phẩm sạch tinh khiết tại phân khu đầu ra:
`data/output/`

### Vận hành trạm kiểm thử tự động

Khi tiến hành thay đổi logic hoặc nâng cấp các lõi lọc, người vận hành cần chạy lệnh sau từ thư mục gốc dự án để giải phóng bộ nhớ đệm cache cũ của Windows và kích hoạt toàn bộ hệ thống kiểm định QA tự động:
`Remove-Item -Recurse -Force (Get-ChildItem -Recurse -Include __pycache__, .pytest_cache) ; pytest -v`

### Nguyên lý duy trì tính Lũy đẳng

Hệ thống thiết kế tách biệt 100% logic lập trình và biểu thức Regex. Mọi hành vi điều chỉnh quy tắc khử nhiễu tiếng Việt chỉ được thực hiện tại tệp `config/rules.json`. Khi khai báo mẫu tìm kiếm trong file JSON, các ký hiệu backreference bắt buộc phải nhân đôi dấu gạch chéo ngược thành `\\1\\2` để trình điều phối phân giải chính xác sang mã Python.

---

## 4. Chính sách Bảo mật Kho lưu trữ (Git Security Policy)

Hệ thống thiết lập hàng rào bảo an nghiêm ngặt nhằm chống rò rỉ tri thức cá nhân lên mạng công cộng:

* **Cô lập bể chứa dữ liệu:** Toàn bộ nội dung nằm trong `data/input/` và `data/output/` bị chặn vĩnh viễn bởi `.gitignore`.

* **Gỡ bỏ chỉ mục theo dõi:** Lịch sử theo dõi của Git (Git Index) đối với hai phân khu này đã được gỡ bỏ hoàn toàn bằng lệnh `--cached` để đảm bảo tính an toàn tuyệt đối khi thực hiện lệnh đẩy mã nguồn.
