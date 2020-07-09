import os
from flask import Flask, json, request
import json
from service import ResponseService

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')

MIN_PAYMENT = app.config['PAYMENT_AMOUNT']
RespService = ResponseService(app.config['PATH_TO_SMILEYCOIND'], MIN_PAYMENT) # path to smileycoin

walleturl = 'https://wallet.smileyco.in/?network=smileycoin' # URL for html5 wallet

app.config.from_pyfile('config.py', silent=True)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

@app.route('/getpaymentlink')
def get_paymentlink():
    return RespService.getnewaddress()

@app.route('/verifypayment/<address>')
def get_transaction(address):
    return RespService.gettransactiondata(address)


if __name__ == "__main__":        # on running python app.py
    app.run()
