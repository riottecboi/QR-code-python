from flask import Flask, render_template, request, url_for, redirect
from flask_wtf.csrf import CSRFProtect
from qr_generator import *

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SESSION_COOKIE_NAME'] = "session"
app.config['SECRET_KEY'] = "supersecretkey"

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('normal'), code=302)


@app.route('/normal', methods=['GET', 'POST'])
def normal():
    if request.method == 'POST':
        input_val = request.form.get('inputText')
        qrcode = normal_generator(input_val)
        return render_template('index.html', qrcode=qrcode, input_val=input_val)
    return render_template('index.html')


if __name__ == '__main__':
    app.run()