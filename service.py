import json
import os


class ResponseService:
    def __init__(self,path_to_smileycoind, payment_amount):
        self.smileyCLI = SmileycoinCLI(path_to_smileycoind)
        self.paymentAmount = payment_amount
        self.walletURL = 'https://wallet.smileyco.in/?network=smileycoin' # URL for html5 wallet


    def getnewaddress(self):
        newaddress = self.smileyCLI.getnewaddress()
        message = ''
        if newaddress == '':
            response = {
            "address": newaddress,
            "amount": self.paymentAmount,
            "link": None,
            "message": 'Failed to connect to smileycoin'
            }
        else:
            response = {
            "address": newaddress,
            "amount": self.paymentAmount,
            "link": self.walletURL + "&address=" + newaddress + "&amount=" + str(self.paymentAmount),
            "message": message
            }
        return response


    def gettransactiondata(self, address):
        output = self.smileyCLI.getreceivedbyaddress(address)
        if "error" in output:
            resp = output
        elif len(output) == 0:
            resp = {
            "amount": 0,
            "confirmations": 0,
            "paid": "no"
            }
        elif len(output) >=1:
            resp = {
            "amount": output[0]['amount'],
            "confirmations": output[0]['confirmations'],
            "paid": "no"
            }
            if output[0]['amount'] >= self.paymentAmount:
                resp['paid'] = 'yes'
        return resp




class SmileycoinCLI:
    def __init__(self, path):
        self.path_to_smileycoind = path

    def getnewaddress(self):
        return os.popen(self.path_to_smileycoind + ' getnewaddress').read().rstrip()

    def getreceivedbyaddress(self, address):
        output = os.popen(self.path_to_smileycoind + ' listunspent 0 999999 "[\\"' + address + '\\"]"').read()
        if output == '':
            return json.loads('{"error": "Invalid Smileycoin address"}')
        else:
            return json.loads(output.rstrip())
