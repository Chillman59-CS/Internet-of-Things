import time
import sys
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from grove.gpio import GPIO
from grove.display.jhd1802 import JHD1802
from seeed_dht import DHT

# ==============================================================================
# CẤU HÌNH THÔNG SỐ THINGSPEAK (GỬI QUA GIAO THỨC MQTT)
# ==============================================================================
CHANNEL_ID = "3519391"          
MQTT_USERNAME = "ORIcMyYfOCAFJzUSMj0wGjs"    
MQTT_CLIENT_ID = "ORIcMyYfOCAFJzUSMj0wGjs" 
MQTT_PASSWORD = "ir5KlVSh3DYrTrD+WoJkDm2R"   
MQTT_BROKER = "mqtt3.thingspeak.com"
MQTT_PORT = 1883

# ==============================================================================
# CẤU HÌNH CHÂN PHẦN CỨNG (GROVE BASE HAT TRÊN RASPBERRY PI)
# ==============================================================================
PIN_RED_LED = 18       # Cổng D18 (LED Đỏ điều khiển theo nhiệt độ)
PIN_YELLOW_LED = 16    # Cổng D16 (LED Vàng điều khiển theo độ ẩm)
PIN_DHT_SENSOR = 5     # Cổng D5  (Cảm biến DHT11 / DHT22)

# ==============================================================================
# LỚP ĐIỀU KHIỂN LED GROVE
# ==============================================================================
class GroveLed(GPIO):
    def __init__(self, pin):
        super(GroveLed, self).__init__(pin, GPIO.OUT)

    def on(self):
        self.write(1)

    def off(self):
        self.write(0)

# ==============================================================================
# HÀM GỬI DỮ LIỆU LÊN THINGSPEAK BẰNG GIAO THỨC MQTT
# ==============================================================================
def publish_via_mqtt(client, temp, humidity):
    """
    Gửi dữ liệu nhiệt độ (field1) và độ ẩm (field2) lên Server ThingSpeak
    sử dụng GIAO THỨC MQTT (Publish to topic).
    """
    topic = f"channels/{CHANNEL_ID}/publish"
    payload = f"field1={temp:.1f}&field2={humidity:.1f}&status=MQTTPUBLISH"
    
    result = client.publish(topic, payload)
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"[MQTT SUCCESS] Đã publish dữ liệu lên Topic '{topic}': Temp={temp:.1f}°C, Humidity={humidity:.1f}%")
    else:
        print(f"[MQTT ERROR] Không thể gửi dữ liệu, mã lỗi: {result.rc}")

# ==============================================================================
# CHƯƠNG TRÌNH CHÍNH (RASPBERRY PI)
# ==============================================================================
def main():
    # Khởi tạo thiết bị ngoại vi
    red_led = GroveLed(PIN_RED_LED)
    yellow_led = GroveLed(PIN_YELLOW_LED)
    dht_sensor = DHT("11", PIN_DHT_SENSOR)  # Đổi sang "22" nếu xài DHT22
    lcd = JHD1802()

    # Khởi tạo MQTT Client
    client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=MQTT_CLIENT_ID
    )
    client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)

    print("===============================================================")
    print("  RASPBERRY PI: GIÁM SÁT NHIỆT ĐỘ - ĐỘ ẨM & GỬI MQTT THINGSPEAK")
    print("===============================================================")
    print("Đang kết nối đến ThingSpeak MQTT Broker (mqtt3.thingspeak.com)...")
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        client.loop_start()
        print("-> Kết nối MQTT Broker thành công!\n")
    except Exception as e:
        print(f"-> Lỗi kết nối MQTT Broker: {e}")
        sys.exit(1)

    red_is_on = False
    yellow_is_on = False

    try:
        while True:
            # 1. Đọc giá trị nhiệt độ và độ ẩm từ cảm biến DHT
            humidity, temp = dht_sensor.read()

            if temp is None or humidity is None:
                print("[WARNING] Lỗi đọc dữ liệu cảm biến DHT! Đang thử lại...")
                time.sleep(2)
                continue

            # 2. Điều khiển LED Đỏ theo Nhiệt độ
            # LED đỏ: Sáng khi nhiệt độ > 30°C, tắt khi nhiệt độ < 25°C
            if temp > 30:
                red_led.on()
                red_is_on = True
            elif temp < 25:
                red_led.off()
                red_is_on = False

            # 3. Điều khiển LED Vàng theo Độ ẩm
            # LED vàng: Sáng khi độ ẩm > 60%, tắt khi độ ẩm < 30%
            if humidity > 60:
                yellow_led.on()
                yellow_is_on = True
            elif humidity < 30:
                yellow_led.off()
                yellow_is_on = False

            # 4. Hiển thị thông tin lên Terminal của Raspberry Pi
            current_time = time.strftime('%H:%M:%S')
            print(f"--- [Time: {current_time}] ---")
            print(f"  + Temp : {temp:.1f}°C  => LED Đỏ  : {'SÁNG' if red_is_on else 'TẮT'}")
            print(f"  + Humi    : {humidity:.1f}%   => LED Vàng: {'SÁNG' if yellow_is_on else 'TẮT'}")

            # 5. Hiển thị lên màn hình LCD 16x2
            lcd.setCursor(0, 0)
            lcd.write(f"Temp: {temp:.1f}C    ")
            lcd.setCursor(1, 0)
            lcd.write(f"Humi: {humidity:.1f}%    ")

            # 6. Gửi dữ liệu lên ThingSpeak qua giao thức MQTT
            publish_via_mqtt(client, temp, humidity)
            print("---------------------------------------------------------------\n")

            # Chu kỳ gửi và hiển thị: 10 giây/lần
            time.sleep(10)

    except KeyboardInterrupt:
        print("\nĐang dừng hệ thống và dọn dẹp phần cứng...")
        red_led.off()
        yellow_led.off()
        lcd.setCursor(0, 0)
        lcd.write("System Stopped  ")
        lcd.setCursor(1, 0)
        lcd.write("                ")
        client.loop_stop()
        client.disconnect()
        print("Đã đóng kết nối MQTT và thoát an toàn.")
        sys.exit(0)

if __name__ == "__main__":
    main()
