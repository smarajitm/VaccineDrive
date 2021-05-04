import requests
import json
import logging
import hashlib
from argparse import ArgumentParser


logger = logging.getLogger()
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

HEADERS = {'Content-type': 'application/json'}

def parse_args():
    """ Define argument parsing

    Returns: args object

    """
    parser = ArgumentParser(
        description='Utility for Booking Covid appointments')

    parser.add_argument('--mobile', help="Mobile Number")
    parser.add_argument('--date', help="date to book appointment in DD-MM-YYYY format")
    parser.add_argument('--pin', help="PINCODE for the location")

    args = parser.parse_args()
    return args

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
            logger.debug("Response from COWIN API for Auth is", txn)
            ''' confirm otp '''
            print("Please provide OTP received on", self.mobile)
            otp = str(input())
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
    args=parse_args()
    mobile = args.mobile
    pin = args.pin
    date = args.date
    r = Runner(mobile, pin, date)
    tok = r.auth()
    if tok == "":
        logger.info("Authentication Failure")
        exit()
    r.find_appointments(pin, date, tok)
