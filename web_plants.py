from flask import Flask, render_template, redirect, url_for
import psutil
import datetime
import water
import os
from flask_basicauth import BasicAuth

app = Flask(__name__)

def template(title = "HELLO!", text = ""):
    now = datetime.datetime.now()
    timeString = now
    templateDate = {
        'title' : title,
        'time' : timeString,
        'text' : text
        }
    return templateDate

app.config['BASIC_AUTH_USERNAME'] = os.environ['USER']
app.config['BASIC_AUTH_PASSWORD'] = os.environ['PASSWORD']

basic_auth = BasicAuth(app)

@basic_auth.required
@app.route("/")
def hello():
    templateData = template()
    return render_template('main.html', **templateData)

@basic_auth.required
@app.route("/last_watered")
def check_last_watered():
    last_watered = water.get_last_watered()
    if "NEVER" not in last_watered:
        laster_watered = f"Last watered: {last_watered}"
    templateData = template(text = last_watered)
    return render_template('main.html', **templateData)

@basic_auth.required
@app.route("/sensor")
def action():
    status = water.get_status()
    message = ""
    if (status == 1):
        message = "Water me please!"
    else:
        message = "I'm a happy plant"

    templateData = template(text = message)
    return render_template('main.html', **templateData)

@basic_auth.required
@app.route("/water")
def action2():
    water.pump_on()
    templateData = template(text = "Watered Once")
    return render_template('main.html', **templateData)

@basic_auth.required
@app.route("/auto/water/<toggle>")
def auto_water(toggle):
    running = False
    if toggle == "ON":
        templateData = template(text = "Auto Watering On")
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1] == 'auto_water.py':
                    templateData = template(text = "Already running")
                    running = True
            except:
                pass
        if not running:
            os.system("python3 auto_water.py&")
    else:
        templateData = template(text = "Auto Watering Off")
        os.system("pkill -f water.py")

    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
