from flask import Flask, render_template, request
import math

app = Flask(__name__)

# Функция для расчета зоны уверенного приема (WiFi, WiMAX, LiFi и других технологий)
def coverage(distance_transmitter, transmitter_power, tx_antenna_gain, rx_antenna_gain, signal_loss, speed_of_light=3e8):
    return math.sqrt((transmitter_power * tx_antenna_gain * rx_antenna_gain) / ((4 * math.pi * distance_transmitter / speed_of_light) ** 2 * signal_loss))

# Функция для расчета зоны уверенного приема LiFi (с учетом мощности светового источника и угла распространения света)
def lifi_coverage(distance_transmitter, transmitter_power, light_source_power, light_angle):
    return math.pi * (distance_transmitter ** 2) * (light_source_power / (4 * math.pi * math.sin(math.radians(light_angle)) ** 2))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_wifi_wimax', methods=['POST'])
def calculate_wifi_wimax():
    distance = float(request.form['distance_wifi_wimax'])
    power = float(request.form['power_wifi_wimax'])
    tx_gain = float(request.form['tx_gain_wifi_wimax'])
    rx_gain = float(request.form['rx_gain_wifi_wimax'])
    loss = float(request.form['loss_wifi_wimax'])

    wifi_zone = coverage(distance, power, tx_gain, rx_gain, loss)

    return render_template('result.html', technology='WiFi/WiMAX', zone=wifi_zone)

@app.route('/calculate_lifi', methods=['POST'])
@app.route('/calculate_lifi', methods=['POST'])
def calculate_lifi():
    try:
        distance = float(request.form['distance_lifi'])
        power = float(request.form['power_lifi'])
        light_power = float(request.form['light_power_lifi'])
        light_angle = float(request.form['light_angle_lifi'])
        
        # Проверка на допустимый диапазон для угла распространения света
        if light_angle < 0 or light_angle > 360:
            raise ValueError("Light propagation angle must be between 0 and 360 degrees")

        lifi_zone = lifi_coverage(distance, power, light_power, light_angle)
        return render_template('result.html', technology='LiFi', zone=lifi_zone)

    except ValueError as e:
        return render_template('error.html', message=str(e))


if __name__ == '__main__':
    app.run(debug=True)
