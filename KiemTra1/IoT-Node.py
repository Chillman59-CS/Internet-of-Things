import time, sys  # Import thư viện thời gian và hệ thống để dùng sleep, exit, và xử lý Ctrl+C
from grove.gpio import GPIO  # Import thư viện GPIO của Grove để điều khiển chân tín hiệu
from grove.adc import ADC  # Import thư viện ADC của Grove để đọc tín hiệu analog từ cảm biến
from grove.display.jhd1802 import JHD1802  # Import thư viện màn hình LCD 16x2 của Grove
import paho.mqtt.client as mqtt  # Import thư viện MQTT để gửi dữ liệu lên server cloud
from paho.mqtt.enums import CallbackAPIVersion  # Import enum phiên bản callback của thư viện MQTT

# --- CẤU HÌNH THINGSPEAK MQTT MỚI ---
CHANNEL_ID = "3510013"  # Mã kênh ThingSpeak để xác định nơi dữ liệu sẽ được gửi
MQTT_USERNAME = "OhYWHDIqBw4lMSgsGzIzCQ8"  # Username MQTT của ThingSpeak
MQTT_CLIENT_ID = "OhYWHDIqBw4lMSgsGzIzCQ8"  # Client ID dùng khi kết nối tới broker MQTT
MQTT_PASSWORD = "1KdzIQ1XKwcMQaj9O3wV6lHc"  # Password MQTT của tài khoản ThingSpeak
MQTT_BROKER = "mqtt3.thingspeak.com"  # Địa chỉ broker MQTT mà chương trình kết nối đến

# --- CẤU HÌNH SƠ ĐỒ CHÂN (GROVE) ---
PIN_ULTRASONIC = 22     # D22 (Cảm biến siêu âm)  # Gán chân GPIO 22 cho cảm biến siêu âm
PIN_RED_LED = 18        # D18 (LED đỏ)  # Gán chân GPIO 18 cho LED đỏ
PIN_YELLOW_LED = 16     # D16 (LED vàng)  # Gán chân GPIO 16 cho LED vàng
SENSOR_LIGHT_PIN = 0    # A0  (Cảm biến ánh sáng)  # Gán kênh ADC 0 cho cảm biến ánh sáng

# --- CLASS ĐIỀU KHIỂN LED ---
class GroveLed(GPIO):  # Tạo lớp con kế thừa từ class GPIO của Grove để điều khiển LED
    def __init__(self, pin):  # Hàm khởi tạo, nhận vào số pin cần điều khiển
        super(GroveLed, self).__init__(pin, GPIO.OUT)  # Gọi constructor cha, đặt pin ở chế độ OUTPUT

    def on(self):  # Hàm bật LED
        self.write(1)  # Ghi giá trị 1 vào pin, tức bật LED

    def off(self):  # Hàm tắt LED
        self.write(0)  # Ghi giá trị 0 vào pin, tức tắt LED

# --- CLASS CẢM BIẾN ÁNH SÁNG ---
class GroveLightSensor:  # Tạo lớp để đọc giá trị ánh sáng từ ADC
    def __init__(self, channel):  # Hàm khởi tạo, lưu kênh ADC cần đọc
        self.channel = channel  # Gán kênh ADC vào thuộc tính channel
        self.adc = ADC()  # Khởi tạo đối tượng ADC để đọc tín hiệu analog

    @property
    def light(self):  # Tạo property light để lấy giá trị ánh sáng dễ dàng
        value = self.adc.read(self.channel)  # Đọc tín hiệu analog từ kênh cảm biến ánh sáng
        return value  # Trả về giá trị ánh sáng đã đọc

# --- CLASS CẢM BIẾN SIÊU ÂM ---
usleep = lambda x: time.sleep(x/1000000.0)  # Hàm trợ giúp làm chậm theo microseconds, dùng cho cảm biến siêu âm
_TIMEOUT1 = 1000  # Giới hạn đếm timeout lần 1 khi chờ tín hiệu phát ra
_TIMEOUT2 = 10000  # Giới hạn đếm timeout lần 2 khi chờ tín hiệu echo quay về

class GroveUltrasonicRanger(object):  # Tạo lớp điều khiển cảm biến siêu âm
    def __init__(self, pin):  # Hàm khởi tạo nhận pin kết nối cảm biến
        self.dio = GPIO(pin)  # Khởi tạo đối tượng GPIO cho chân cảm biến

    def _get_distance(self):  # Hàm nội bộ để đo khoảng cách
        self.dio.dir(GPIO.OUT)  # Đặt chân cảm biến ở chế độ OUTPUT để phát sóng
        self.dio.write(0)  # Gửi tín hiệu LOW để reset chân
        usleep(2)  # Chờ 2 micro giây
        self.dio.write(1)  # Gửi tín hiệu HIGH để bắt đầu phát xung
        usleep(10)  # Giữ xung phát trong 10 micro giây
        self.dio.write(0)  # Tắt xung phát

        self.dio.dir(GPIO.IN)  # Đổi chân sang chế độ INPUT để đợi tín hiệu echo

        t0 = time.time()  # Ghi thời điểm bắt đầu chờ tín hiệu
        count = 0  # Biến đếm để kiểm tra timeout
        while count < _TIMEOUT1:  # Lặp cho đến khi timeout 1
            if self.dio.read():  # Nếu chân nhận được tín hiệu HIGH, tức bắt đầu echo
                break  # Thoát vòng lặp
            count += 1  # Tăng đếm nếu chưa có tín hiệu

        if count >= _TIMEOUT1:  # Nếu hết thời gian mà không có echo
            return None  # Trả về None để báo lỗi/không đo được

        t1 = time.time()  # Ghi thời điểm bắt đầu đo độ dài của tín hiệu echo
        count = 0  # Reset biến đếm
        while count < _TIMEOUT2:  # Lặp cho đến khi timeout 2
            if not self.dio.read():  # Nếu tín hiệu echo kết thúc (đổi từ HIGH xuống LOW)
                break  # Thoát vòng lặp
            count += 1  # Tăng đếm khi còn đang nhận tín hiệu

        if count >= _TIMEOUT2:  # Nếu chờ quá lâu mà không thấy echo kết thúc
            return None  # Trả về None

        t2 = time.time()  # Ghi thời điểm kết thúc đo echo

        dt = int((t1 - t0) * 1000000)  # Tính thời gian từ lúc phát xung đến lúc nhận echo đầu tiên

        if dt > 530:  # Nếu thời gian quá dài, chứng tỏ không có vật thể hoặc cảm biến lỗi
            return None  # Bỏ qua kết quả đo không hợp lệ

        distance = ((t2 - t1) * 1000000 / 29 / 2)  # Công thức tính khoảng cách theo thời gian echo
        return distance  # Trả về khoảng cách tính được theo cm

    def get_distance(self):  # Hàm công khai để lấy khoảng cách
        while True:  # Lặp vô hạn để giữ cho việc đo khoảng cách luôn hoạt động
            dist = self._get_distance()  # Gọi hàm đo khoảng cách bên trong
            if dist:  # Nếu khoảng cách nhận được hợp lệ
                return dist  # Trả về giá trị khoảng cách

# --- HÀM GỬI DỮ LIỆU SANG THINGSPEAK ---
def thingspeak_mqtt_publish(client, light_val, dist_val):  # Hàm gửi dữ liệu cảm biến lên ThingSpeak qua MQTT
    payload = f"field1={light_val}&field2={dist_val:.1f}&status=MQTTPUBLISH"  # Tạo chuỗi dữ liệu theo định dạng mà ThingSpeak chấp nhận
    client.publish(f"channels/{CHANNEL_ID}/publish", payload)  # Gửi payload lên kênh MQTT của ThingSpeak

# --- KHỞI TẠO CÁC THIẾT BỊ ---
red_led = GroveLed(PIN_RED_LED)  # Khởi tạo đối tượng LED đỏ ở chân GPIO 18
yellow_led = GroveLed(PIN_YELLOW_LED)  # Khởi tạo đối tượng LED vàng ở chân GPIO 16
light_sensor = GroveLightSensor(SENSOR_LIGHT_PIN)  # Khởi tạo cảm biến ánh sáng ở kênh A0
sonar = GroveUltrasonicRanger(PIN_ULTRASONIC)  # Khởi tạo cảm biến siêu âm ở chân GPIO 22
lcd = JHD1802()  # Khởi tạo màn hình LCD 16x2

# Khởi tạo MQTT Client
client = mqtt.Client(  # Tạo đối tượng client MQTT để kết nối với broker
    callback_api_version=CallbackAPIVersion.VERSION2,  # Chọn phiên bản callback API 2.0 của thư viện MQTT
    client_id=MQTT_CLIENT_ID  # Đặt client ID cho kết nối MQTT
)

client.username_pw_set(  # Thiết lập username và password để đăng nhập broker MQTT
    username=MQTT_USERNAME,  # Username của tài khoản ThingSpeak
    password=MQTT_PASSWORD  # Password của tài khoản ThingSpeak
)

client.connect(MQTT_BROKER, 1883, 60)  # Kết nối tới broker MQTT ở cổng 1883, timeout 60 giây
client.loop_start()  # Khởi động thread MQTT nền để nhận/gửi dữ liệu liên tục

# Biến lưu trạng thái bật/tắt của LED
red_is_on = False  # Biến trạng thái LED đỏ, mặc định tắt
yellow_is_on = False  # Biến trạng thái LED vàng, mặc định tắt

print("Dang chay chuong trinh tren Raspberry Pi...")  # In ra terminal thông báo chương trình đang chạy

try:  # Bắt lỗi nếu người dùng nhấn Ctrl+C hoặc có ngoại lệ xảy ra
    while True:  # Vòng lặp vô hạn để chương trình chạy liên tục
        # 1. Đọc giá trị từ cảm biến
        light_val = light_sensor.light  # Đọc giá trị cường độ ánh sáng từ cảm biến ánh sáng
        dist_val = sonar.get_distance()  # Đọc khoảng cách từ cảm biến siêu âm

        # 2. Xử lý logic LED đỏ (Hysteresis Ánh sáng)
        if light_val > 500:  # Nếu ánh sáng quá sáng, bật LED đỏ
            red_led.on()  # Gọi hàm bật LED đỏ
            red_is_on = True  # Cập nhật trạng thái LED đỏ là đang sáng
        elif light_val < 300:  # Nếu sáng yếu quá, tắt LED đỏ
            red_led.off()  # Gọi hàm tắt LED đỏ
            red_is_on = False  # Cập nhật trạng thái LED đỏ là tắt

        # 3. Xử lý logic LED vàng (Hysteresis Khoảng cách)
        if dist_val < 10:  # Nếu vật thể gần quá (dưới 10 cm), bật LED vàng
            yellow_led.on()  # Gọi hàm bật LED vàng
            yellow_is_on = True  # Cập nhật trạng thái LED vàng là sáng
        elif dist_val > 30:  # Nếu khoảng cách lớn hơn 30 cm, tắt LED vàng
            yellow_led.off()  # Gọi hàm tắt LED vàng
            yellow_is_on = False  # Cập nhật trạng thái LED vàng là tắt

        # 4. In thông tin ra Terminal
        print(f"\n--- Du lieu ({time.strftime('%H:%M:%S')}) ---")  # In tiêu đề thời gian hiện tại ra terminal
        print(  # In dòng thông tin ánh sáng và trạng thái LED đỏ
            f"Cuong do anh sang: {light_val} | "  # Phần mô tả cường độ ánh sáng
            f"LED Do: {'SANG' if red_is_on else 'TAT'}"  # Hiển thị trạng thái LED đỏ đang sáng hay tắt
        )
        print(  # In dòng thông tin khoảng cách và trạng thái LED vàng
            f"Khoang cach: {dist_val:.1f} cm | "  # Phần mô tả khoảng cách đo được
            f"LED Vang: {'SANG' if yellow_is_on else 'TAT'}"  # Hiển thị trạng thái LED vàng
        )

        # 5. Hiển thị thông tin lên LCD 16x2
        lcd.setCursor(0, 0)  # Đưa con trỏ LCD về dòng 1, cột 0
        lcd.write(f"Light: {light_val:<10}")  # Ghi cường độ sáng lên dòng 1 LCD

        lcd.setCursor(1, 0)  # Đưa con trỏ LCD về dòng 2, cột 0
        lcd.write(f"Dist: {dist_val:.1f}cm     ")  # Ghi khoảng cách lên dòng 2 LCD, thêm khoảng trắng để xóa dữ liệu cũ

        # 6. Gửi dữ liệu lên ThingSpeak qua MQTT
        thingspeak_mqtt_publish(client, light_val, dist_val)  # Gọi hàm gửi dữ liệu lên cloud

        # Chờ 15 giây theo yêu cầu đề bài
        time.sleep(15)  # Tạm dừng chương trình 15 giây trước khi đọc lại dữ liệu

except KeyboardInterrupt:  # Nếu người dùng nhấn Ctrl+C để dừng chương trình
    red_led.off()  # Tắt LED đỏ khi thoát
    yellow_led.off()  # Tắt LED vàng khi thoát
    client.loop_stop()  # Dừng vòng lặp MQTT nền
    client.disconnect()  # Ngắt kết nối MQTT
    print("\nThoat chuong trinh thanh cong!")  # In thông báo thoát thành công
    sys.exit(0)  # Kết thúc chương trình với mã thoát 0