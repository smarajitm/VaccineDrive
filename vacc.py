import requests
import json

def auth(mobile):
    data = {'mobile':mobile}
    headers = {'Content-type': 'application/json'}
    r = requests.post('https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP', headers=headers, json=data)
    
    if r.ok:
        respJson = r.json()

        txn = respJson['txnId']
        print(txn)
        ''' confirm otp '''
        otp = input()
        data = {"otp": otp, "txnId": txn}
        r = requests.post('https://cdn-api.co-vin.in/api/v2/auth/public/confirmOTP', headers=headers, json=data)
        if r.ok:
            x = r.json()
            token = x['token']
            return token
        else:
            print(r.text)
    else:
        print(r.text)
    return ""


def find_appointments(pin, date, tok):
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPini?pincode={}&date={}".format(pin,date)
    headers = {'Content-type': 'application/json'}
    r = requests.get(url=URL, headers=headers ,auth=(tok,''))
    print(r)
    print(r.json())
    respJson = r.json()

    sessions = respJson['sessions']

    for sess in sessions:
        if sess['available_capacity'] > 0 and sess['min_age_limit'] == 18:
            print("session available")
            print(sess)
     



if __name__ == "__main__":
    mobile=""
    pin="560048"
    date="04-05-2021"
    tok = auth(mobile)
    if tok == "":
        print("Authentication Failure")
        exit()
    find_appointments(pin, date, tok)


