from urllib import request  # Import module request của urllib để thực hiện HTTP request
from time import sleep  # Import hàm sleep để tạm dừng chương trình theo thời gian
import json  # Import json để chuyển dữ liệu JSON thành Python dict

# --- CẤU HÌNH THINGSPEAK ---
CHANNEL_ID = "3510013"  # ID kênh ThingSpeak chứa dữ liệu cảm biến
READ_API_KEY = "KX3HRUMKYZRJFX3A"  # API key đọc dữ liệu từ kênh ThingSpeak

# --- HÀM LẤY DỮ LIỆU HTTP GET ---
def thingspeak_get():  # Hàm này dùng HTTP GET để lấy dữ liệu mới nhất từ ThingSpeak
    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds/last.json?api_key={READ_API_KEY}"  # Tạo URL API của ThingSpeak để lấy feed mới nhất
    req = request.Request(url, method="GET")  # Tạo request HTTP theo phương thức GET
    r = request.urlopen(req)  # Gửi request và nhận phản hồi từ server
    response_data = r.read().decode()  # Đọc dữ liệu trả về dưới dạng bytes rồi chuyển thành string
    response_data = json.loads(response_data)  # Chuyển chuỗi JSON thành dictionary Python để dễ xử lý
    return response_data  # Trả về dữ liệu JSON đã parse


print("CHUONG TRINH GIAM SAT DU LIEU TU XA (PC / LAPTOP)")  # In tiêu đề chương trình giám sát dữ liệu từ xa
print("Dang ket noi va lang nghe du lieu tu ThingSpeak...\n")  # In thông báo đang kết nối và chờ dữ liệu

last_entry_id = None  # Biến lưu entry_id cuối cùng đã được hiển thị, dùng để tránh lặp dữ liệu cũ

while True:  # Vòng lặp vô hạn để chương trình chạy liên tục
    try:  # Bắt lỗi nếu có sự cố kết nối hoặc đọc dữ liệu
        data = thingspeak_get()  # Gọi hàm lấy dữ liệu từ ThingSpeak
        entry_id = data.get("entry_id")  # Lấy mã bản ghi mới nhất từ dữ liệu JSON

        # Chi in khi co du lieu ban ghi moi cap nhat
        if entry_id != last_entry_id and entry_id is not None:  # Chỉ in nếu entry_id khác với giá trị trước đó và không rỗng
            last_entry_id = entry_id  # Cập nhật entry_id gần nhất đã xử lý

            created_at = data.get("created_at")  # Lấy thời gian dữ liệu được tạo
            light_val = data.get("field1")  # Lấy giá trị cường độ ánh sáng từ field1
            dist_val = data.get("field2")  # Lấy giá trị khoảng cách từ field2

            print(f"[{created_at}] - Cap nhat Entry #{entry_id}:")  # In thời gian và mã bản ghi cập nhật
            print(f"  * Cuong do anh sang (Field 1): {light_val}")  # In giá trị ánh sáng
            print(f"  * Khoang cach vat can (Field 2): {dist_val} cm")  # In khoảng cách vật cản
            print("-" * 50)  # In dòng phân cách để dễ đọc màn hình

    except Exception as e:  # Nếu có lỗi thì bắt và in lỗi ra màn hình
        print("Loi khi ket noi/doc du lieu tu ThingSpeak:", e)  # In thông báo lỗi + chi tiết lỗi

    # Dinh ky doc du lieu moi 5 giay
    sleep(5)  # Dừng 5 giây rồi đọc lại dữ liệu để cập nhật định kỳ