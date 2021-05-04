import requests
import json
import logging
import hashlib


logger = logging.getLogger()
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

HEADERS = {'Content-type': 'application/json'}


class Runner:
    def __init__(self, mobile, pincode, date):
        logger.info("Runner created")
        self.mobile = mobile
        self.pincode = pincode
        self.date = date

    def auth(self):
        data = {'mobile': self.mobile}
        r = requests.post(
            'https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP', headers=HEADERS, json=data)

        if r.ok:
            respJson = r.json()
            txn = respJson['txnId']
            logger.debug("Response from COWIN API for Auth is %s", txn)
            ''' confirm otp '''
            print("Please provide OTP received on %s", self.mobile)
            otp = input()
            data = {"otp": hashlib.sha256(
                otp.encode('utf-8')).hexdigest(), "txnId": txn}
            logger.debug("Payload for Confirm OTP is %s", data)
            r = requests.post(
                'https://cdn-api.co-vin.in/api/v2/auth/public/confirmOTP', headers=HEADERS, json=data)
            if r.ok:
                x = r.json()
                token = x['token']
                return token
            else:
                logger.debug(r)
                logger.debug(r.text)
        else:
            logger.debug(r.text)
        return ""

    def find_appointments(self, pin, date, tok):
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPini?pincode={}&date={}".format(
            pin, date)
        r = requests.get(url=URL, headers=HEADERS, auth=(tok, ''))
        logger.debug(r)
        logger.debug(r.json())
        respJson = r.json()
        sessions = respJson['sessions']

        for sess in sessions:
            if sess['available_capacity'] > 0 and sess['min_age_limit'] == 18:
                logger.debug("session available")
                logger.debug(sess)


if __name__ == "__main__":
    print("Please provide phone number")
    mobile = input()
    print("Please provide pin code")
    pin = input()
    print("Please provide date as DD-MM-YYYY")
    date = input()
    r = Runner(mobile, pin, date)
    tok = r.auth()
    if tok == "":
        logger.info("Authentication Failure")
        exit()
    r.find_appointments(pin, date, tok)
