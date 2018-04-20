from flask import Flask
from flask import render_template
import sys
import sqlite3
app = Flask(__name__)
conn = sqlite3.connect('example.db')


def save_data(zone,temp):
    conn = sqlite3.connect('temps.db')
    try:
        conn.execute("insert into temps (tdate,ttime,zone,temperature) values (?, ?, ?, ?)",
                 (date.today(),
                  datetime.now().strftime("%H:%M:%S"),
                  zone,
                  temp))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_data():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.execute("SELECT tdate,ttime,zone,temperature from temps")
    data = [row for row in cursor]
    conn.close()
    return data

def get_zone_data(zone):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.execute("SELECT tdate,ttime,zone,temperature from temps WHERE zone = ?",(zone,))
    data = [row for row in cursor]
    conn.close()
    return data

def get_zones():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.execute("select distinct zone from temps;")
    data = [row[0] for row in cursor]
    conn.close()
    return data

@app.route('/temp_register', methods=['GET', 'POST'])
def temp_register():
    if request.method == 'GET':
            return render_template('frontend.html')
    elif request.method == 'POST':
        zone = request.form.get('varzona')
        temp = request.form.get('vartemp')
        if save_data(zone,temp):
            return redirect(url_for('frontend'))
        else:
            return "Error inserting temperature"

@app.route('/hist_data', methods=['GET', 'POST'])
def hist_data():
    historical_data = get_data()
    return render_template('historical_data_table.html',historical_data=historical_data)

@app.route('/zone_data', methods=['GET', 'POST'])
def zone_data():
    zones = get_zones()
    if request.method == 'GET':
        zone_data = []
    elif request.method == 'POST':
        zone = request.form.get('area')
        print(zone)
        zone_data = get_zone_data(zone)
    return render_template('zone_data_table.html',zone_data=zone_data, zones=zones)

if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0")
