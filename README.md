# PHCN AI 2.0 – Tab 5 đối soát chẩn đoán hai chiều tự động

## Mục tiêu phiên bản
- Giữ nguyên 4 tab cũ và các trường nhập liệu hiện có.
- Bổ sung Tab 5: **Đối soát chẩn đoán**.
- Tab 5 tự động lấy dữ liệu khám hiện hành từ Tab 3, không yêu cầu nhập lại.
- Nếu dữ liệu đã thay đổi sau lần phân tích gần nhất, Tab 5 chặn kết quả cũ và yêu cầu phân tích lại.

## Cấu trúc thư mục
- `app.py`: giao diện Streamlit; giữ nguyên các trường nhập liệu cũ, thêm tab thứ năm.
- `clinical_engine.py`: động cơ suy luận offline hiện có.
- `diagnostic_audit.py`: động cơ đối soát hai chiều tự động theo vùng giải phẫu.
- `storage.py`: lưu hồ sơ và lần khám SQLite cục bộ.
- `requirements.txt`: thư viện cần cài.
- `tests/test_diagnostic_audit.py`: kiểm thử logic đối soát.

## Cơ chế Tab 5
1. **Chiều thuận:** từ bệnh sử, triệu chứng, khám và test được ghi dương tính, tạo danh sách giả thuyết có dữ kiện gợi ý.
2. **Chiều ngược:** với từng giả thuyết, kiểm tra lại dấu hiệu ủng hộ, dữ kiện chống lại và những dấu hiệu chưa được ghi nhận/cần khám thêm.
3. **Đối chiếu mâu thuẫn:** kiểm tra một số bất nhất giữa bệnh sử và trường hướng lan; phát hiện giới hạn của trường test.
4. **Chống kết quả cũ:** so sánh chữ ký dữ liệu hiện hành với lần phân tích gần nhất; nếu khác nhau, không cho dùng báo cáo cũ.

Các nhóm vùng được hỗ trợ trong Tab 5: cột sống cổ, cột sống thắt lưng, vai, khuỷu, cổ tay-bàn tay, háng, gối, cổ chân-bàn chân, thần kinh & khác.

## Giới hạn chuyên môn quan trọng
- Đây là hệ thống luật/từ khóa minh bạch để hỗ trợ rà soát, **không phải mô hình đã được thẩm định lâm sàng**.
- Không tính xác suất chẩn đoán, LR, độ nhạy hoặc độ đặc hiệu; không có cơ sở dữ liệu nghiên cứu gắn với từng luật trong bản này.
- Không tìm thấy một dấu hiệu trong ghi chép không có nghĩa dấu hiệu đó âm tính.
- Giao diện test cũ đang gộp “Chưa làm / Âm tính (-)”. Để không thay đổi đầu vào, engine xem lựa chọn này là **chưa xác định**, không dùng để loại trừ bệnh.
- Các cụm từ tự do có thể gây nhận diện thiếu hoặc nhầm; bác sĩ phải xác minh bệnh sử, kỹ thuật test, khám thần kinh/chức năng và cận lâm sàng khi có chỉ định.
- Có cờ đỏ thì ưu tiên đánh giá an toàn, không để Tab 5 tạo cảm giác đã loại trừ nguy cơ.

## Cài đặt và chạy
1. Giải nén ZIP.
2. Cài Python 3.10 trở lên.
3. Mở CMD/Terminal tại thư mục có `app.py`.
4. Chạy: `pip install -r requirements.txt`
5. Chạy: `streamlit run app.py`

## Kiểm thử
Chạy: `python -m unittest discover -s tests -v`

Kiểm thử cú pháp và logic offline không thay thế kiểm thử giao diện trên thiết bị đích hoặc thẩm định lâm sàng.

## Dữ liệu và sao lưu
- SQLite được tạo trong `data/phcn_ai.db` khi chạy lần đầu.
- Không xóa thư mục `data/` khi cập nhật phiên bản.
- Sao lưu thư mục `data/` trước khi thay phiên bản; file này có thể chứa thông tin định danh và dữ liệu sức khỏe.
- Ảnh tải lên không được lưu trong SQLite.
