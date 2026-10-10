import time
import json
import sys
from urllib import request, error

# ==============================================================================
# CẤU HÌNH THÔNG SỐ THINGSPEAK (ĐỌC QUA GIAO THỨC HTTP REST API)
# ==============================================================================
CHANNEL_ID = "3519391"        # Thay bằng Channel ID của bạn trên ThingSpeak
READ_API_KEY = "NS632AXXD12YRDWA"    # Thay bằng Read API Key của Channel
HTTP_INTERVAL = 20                     # Khoảng thời gian đọc dữ liệu (20 giây)

# URL API của ThingSpeak để lấy dữ liệu mới nhất (Last Feed) qua giao thức HTTP GET
THINGSPEAK_HTTP_URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds/last.json?api_key={READ_API_KEY}"

def fetch_data_via_http():
    """
    Gửi truy vấn HTTP GET đến REST API của ThingSpeak để lấy bản ghi mới nhất.
    """
    try:
        req = request.Request(THINGSPEAK_HTTP_URL, headers={'User-Agent': 'Python-PC-Monitor'})
        with request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data_bytes = response.read()
                data_json = json.loads(data_bytes.decode('utf-8'))
                return data_json
            else:
                print(f"[HTTP ERROR] Server trả về mã lỗi: {response.status}")
                return None
    except error.URLError as e:
        print(f"[HTTP CONNECTION ERROR] Không thể kết nối đến ThingSpeak: {e}")
        return None
    except Exception as e:
        print(f"[UNKNOWN ERROR] Lỗi xử lý dữ liệu: {e}")
        return None

def main():
    print("===============================================================")
    print("  PC / LAPTOP: ĐỌC DỮ LIỆU TỪ THINGSPEAK QUA GIAO THỨC HTTP    ")
    print("===============================================================")
    print(f"Target Channel ID : {CHANNEL_ID}")
    print(f"Phương thức       : HTTP GET REST API")
    print(f"Chu kỳ cập nhật   : {HTTP_INTERVAL} giây/lần")
    print("===============================================================\n")

    last_entry_id = None

    try:
        while True:
            # 1. Gọi hàm HTTP GET đọc dữ liệu từ ThingSpeak
            feed = fetch_data_via_http()

            if isinstance(feed, dict) and feed:
                entry_id = feed.get("entry_id")
                created_at = feed.get("created_at", "N/A")
                temp_str = feed.get("field1")
                humi_str = feed.get("field2")

                # Kiểm tra nếu có dữ liệu mới (dựa vào entry_id)
                if entry_id != last_entry_id:
                    last_entry_id = entry_id
                    
                    try:
                        temp = float(temp_str) if temp_str is not None else None
                        humi = float(humi_str) if humi_str is not None else None
                    except ValueError:
                        temp, humi = None, None

                    print(f"[{time.strftime('%H:%M:%S')}] Nhận bản ghi mới thành công (HTTP GET)!")
                    print(f"  + Entry ID  : #{entry_id}")
                    print(f"  + Thời gian : {created_at}")
                    if temp is not None and humi is not None:
                        print(f"  + Nhiệt độ  : {temp:.1f} °C")
                        print(f"  + Độ ẩm     : {humi:.1f} %")
                    else:
                        print(f"  + Giá trị   : Field1={temp_str}, Field2={humi_str}")
                    print("---------------------------------------------------------------")
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] Chưa có dữ liệu mới từ Server ThingSpeak (Entry ID #{entry_id})...")
            else:
                print(
                    f"[{time.strftime('%H:%M:%S')}] "
                    f"Dữ liệu ThingSpeak không hợp lệ: {feed!r}"
                )

            # Chờ 10 giây cho lần gửi yêu cầu HTTP tiếp theo
            time.sleep(HTTP_INTERVAL)

    except KeyboardInterrupt:
        print("\n[INFO] Đã dừng chương trình trên PC/Laptop.")
        sys.exit(0)

if __name__ == "__main__":
    main()