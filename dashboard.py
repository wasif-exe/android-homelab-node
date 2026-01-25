import subprocess
import json
import time
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

BAT_CAPACITY_FILE = "/sys/class/power_supply/battery/capacity"
BAT_TEMP_FILE = "/sys/class/power_supply/battery/temp"

history = {'labels': [], 'temps': []}

def read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read().strip()
    except PermissionError:
        try:
            cmd = subprocess.run(['sudo', 'cat', path], stdout=subprocess.PIPE, timeout=1)
            return cmd.stdout.decode('utf-8').strip()
        except:
            return None
    except:
        return None

def get_stats():
    battery = read_file(BAT_CAPACITY_FILE)
    raw_temp = read_file(BAT_TEMP_FILE)
    
    if battery and raw_temp:
        temp = int(raw_temp) / 10 
        status = "Kernel Mode"
        bat_percent = int(battery)
    else:
        bat_percent = 0
        temp = 0
        status = "Sensor Error"

    try:
        ram_cmd = subprocess.run(['free', '-m'], stdout=subprocess.PIPE)
        ram_out = ram_cmd.stdout.decode('utf-8').splitlines()[1].split()
        ram_total = int(ram_out[1])
        ram_used = int(ram_out[2])
        ram_percent = round((ram_used / ram_total) * 100, 1)
    except:
        ram_used, ram_total, ram_percent = 0, 0, 0

    return {
        "battery": bat_percent,
        "temp": temp,
        "status": status,
        "ram_used": ram_used,
        "ram_total": ram_total,
        "ram_percent": ram_percent
    }

@app.route('/api/data')
def api_data():
    stats = get_stats()
    
    current_time = time.strftime("%H:%M:%S")
    history['labels'].append(current_time)
    history['temps'].append(stats['temp'])
    if len(history['labels']) > 20:
        history['labels'].pop(0)
        history['temps'].pop(0)
        
    return jsonify({**stats, "history": history})

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>OnePlus Core</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body { background-color: #000000; color: #e0e0e0; font-family: monospace; text-align: center; margin: 0; padding: 10px; }
            .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }
            .card { background: #111; border: 1px solid #333; border-radius: 8px; padding: 15px; }
            .big { font-size: 32px; font-weight: bold; margin: 5px 0; }
            .green { color: #0f0; } .orange { color: #fa0; } .blue { color: #0af; }
            canvas { max-height: 200px; }
        </style>
    </head>
    <body>
        <h3 style="border-bottom: 2px solid #333; padding-bottom: 10px;">SYSTEM STATUS</h3>
        
        <div class="grid">
            <div class="card" style="grid-column: span 2">
                <div>RAM LOAD</div>
                <div class="big blue" id="ram">--%</div>
                <small id="ram-detail">-- / -- MB</small>
            </div>
            <div class="card">
                <div>BATTERY</div>
                <div class="big green" id="bat">--%</div>
            </div>
            <div class="card">
                <div>TEMP</div>
                <div class="big orange" id="temp">--°C</div>
            </div>
        </div>

        <div class="card">
            <div>THERMAL HISTORY</div>
            <canvas id="tempChart"></canvas>
        </div>

        <script>
            const ctx = document.getElementById('tempChart').getContext('2d');
            const chart = new Chart(ctx, {
                type: 'line',
                data: { labels: [], datasets: [{ label: 'Temp', borderColor: '#fa0', borderWidth: 2, data: [], tension: 0.4 }] },
                options: { scales: { x: {display:false}, y: {grid: {color: '#222'}} }, plugins: {legend: {display: false}} }
            });

            function updateData() {
                fetch('/api/data')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('bat').innerText = data.battery + '%';
                        document.getElementById('temp').innerText = data.temp + '°C';
                        document.getElementById('ram').innerText = data.ram_percent + '%';
                        document.getElementById('ram-detail').innerText = data.ram_used + ' / ' + data.ram_total + ' MB';

                        chart.data.labels = data.history.labels;
                        chart.data.datasets[0].data = data.history.temps;
                        chart.update();
                    });
            }

            setInterval(updateData, 2000);
            updateData();
        </script>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
