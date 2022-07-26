from flask import Flask, render_template, request, url_for, redirect
from flask_wtf.csrf import CSRFProtect
from qr_generator import *

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SESSION_COOKIE_NAME'] = "session"
app.config['SECRET_KEY'] = "supersecretkey"

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('qr'), code=302)


@app.route('/qr', methods=['GET', 'POST'])
def qr():
    if request.method == 'POST':
        if request.args.get('type') == 'normal':
            input_val = request.form.get('inputText')
            qrcode = normal_generator(input_val)
            return render_template('index.html', qrcode=qrcode)
        elif request.args.get('type') == 'wifi':
            ssid = request.form.get('ssid')
            pwd = request.form.get('password')
            qrcode = wifi_generator(ssid, pwd)
            return render_template('wifi.html', qrcode=qrcode)
    if 'type' in request.args:
        if request.args.get('type') == 'normal':
            return render_template('index.html')
        elif request.args.get('type') == 'wifi':
            return render_template('wifi.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run()