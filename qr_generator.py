import segno
from segno import helpers
import qrcode_artistic

def normal_generator(input):
    qrcode = segno.make(input, micro=False)
    return qrcode

def wifi_generator(ssid, password):
    qrcode = helpers.make_wifi(ssid=str(ssid), password=str(password), security='WPA')
    return qrcode

def geographic_generator(lat, long):
    qrcode = helpers.make_geo(lat, long)
    return qrcode


def artistic_generator(input, output, path):
    qrcode = segno.make(input, micro=False, error='h')
    qrcode_artistic.write_artistic(qrcode, background=path, target=output, scale=3)
    return path


def infomation_card_generator(input_json, type):
    if type == 'vcard':
        qrcode = helpers.make_vcard(name=input_json['name'], displayname=input_json['displayname'], email=input_json['email'],
                                    phone=input_json['phone'], birthday=input_json['birthday'], url=input_json['url'], memo=input_json['memo'])

    elif type == 'mecard':
        qrcode = helpers.make_mecard(name=input_json['name'], nickname=input_json['displayname'], email=input_json['email'],
                                    phone=input_json['phone'], birthday=input_json['birthday'], url=input_json['url'],
                                    memo=input_json['memo'])
    else:
        qrcode = None
    return qrcode