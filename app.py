from flask import Flask, render_template, request, url_for, redirect
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
import os
import base64
from qr_generator import *

app = Flask(__name__)
csrf = CSRFProtect(app)

app.config['SESSION_COOKIE_NAME'] = "session"
app.config['SECRET_KEY'] = "supersecretkey"
app.config['UPLOAD_FOLDER'] = '/tmp'

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('qr'), code=302)


@app.route('/qr', methods=['GET', 'POST'])
def qr():
    if request.method == 'POST':
        try:
            if request.args.get('type') == 'normal':
                input_val = request.form.get('inputText')
                qrcode = normal_generator(input_val)
                return render_template('index.html', qrcode=qrcode)
            elif request.args.get('type') == 'wifi':
                ssid = request.form.get('ssid')
                pwd = request.form.get('password')
                qrcode = wifi_generator(ssid, pwd)
                return render_template('wifi.html', qrcode=qrcode)
            elif request.args.get('type') == 'geographic':
                latitude = request.form.get('latitude')
                longitude = request.form.get('longitude')
                qrcode = geographic_generator(float(latitude), float(longitude))
                return render_template('geographic.html', qrcode=qrcode)
            elif request.args.get('type') == 'artistic':
                input_val = request.form.get('inputText')
                uploaded_file = request.files['file']
                filename = secure_filename(uploaded_file.filename)
                if filename != '':
                    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    uploaded_file.save(path)
                    qr_path = artistic_generator(input=input_val, path=path, output=path)
                    with open(qr_path, "rb") as img:
                        encoded_string = base64.b64encode(img.read()).decode()
                    os.remove(qr_path)
                    return render_template('artistic.html', qrcode=encoded_string)
            elif request.args.get('type') == 'card':
                infomation = {}
                infomation['name'] = request.form.get('name')
                infomation['displayname'] = request.form.get('nickname')
                infomation['email'] = request.form.get('email')
                infomation['phone'] = request.form.get('phone')
                infomation['url'] = request.form.get('url')
                infomation['memo'] = request.form.get('memo')
                vcard_qrcode, mecard_qrcode = infomation_card_generator(infomation)
                return render_template('infocard.html', vcard_qrcode=vcard_qrcode, mecard_qrcode=mecard_qrcode)

            return render_template('index.html')
        except Exception as e:
            print(str(e))
            return render_template('loading.html', message='Error Occurred',
                                   redirect=url_for('index'))

    if 'type' in request.args:
        if request.args.get('type') == 'normal':
            return render_template('index.html')
        elif request.args.get('type') == 'wifi':
            return render_template('wifi.html')
        elif request.args.get('type') == 'geographic':
            return render_template('geographic.html')
        elif request.args.get('type') == 'artistic':
            return render_template('artistic.html')
        elif request.args.get('type') == 'card':
            return render_template('infocard.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run()