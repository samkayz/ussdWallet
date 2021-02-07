import requests
import json
import random
import string
from requests.auth import HTTPBasicAuth


username = "ilemobayosamson@gmail.com"
password = "12345678"
urls = 'https://sandbox.vtpass.com'



class Utility:
    def buy_airtime(self, network, amount, mobile):
        H = 6
        res = ''.join(random.choices(string.digits, k=H))
        txn = str(res)
        txt_id = "TX" + txn

        url = f'{urls}/api/pay'

        payload = {
        "request_id": txt_id,
        "serviceID": network,
        "amount": amount,
        "phone": mobile 
        }
        headers = {
        'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, auth=HTTPBasicAuth(username, password), headers=headers, data = json.dumps(payload))
            #print(response.text.encode('utf8'))
        d_dict = json.loads(response.text)
        # print(d_dict)
        return d_dict


    def Data(self, d_pack, m_no, sel_pack, amount):
        H = 6
        res = ''.join(random.choices(string.digits, k=H))
        txn = str(res)
        txt_id = "TX" + txn
        url = f'{urls}/api/pay'

        payload = {
            "request_id": txt_id,
            "serviceID": d_pack,
            "billersCode": m_no,
            "variation_code": sel_pack,
            "amount": str(amount),
            "phone": m_no 
            }
        headers = {
            'Content-Type': 'application/json',
            }

        response = requests.request("POST", url, auth=HTTPBasicAuth(username, password), headers=headers, data = json.dumps(payload))

        #print(response.text.encode('utf8'))
        d_dict = json.loads(response.text)
        f = []
        for j in d_dict:
            dat = d_dict[j]
            data_ = f.append(dat)
        data_resp = f[1]
        return data_resp


    def tvVerify(self, cardNo, biller):

        url = f'{urls}/api/merchant-verify'

        payload = {
            "billersCode" : cardNo,
            "serviceID" : biller
            }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, auth=HTTPBasicAuth(username, password), headers=headers, data = json.dumps(payload))

        #print(response.text.encode('utf8'))
        d_dict = json.loads(response.text)
        f = []
        for j in d_dict:
            tv = d_dict[j]
            s_tv = f.append(tv)
        tv_resp = f[1]
        return tv_resp


    def PayTV(self, mobile, amount, variation_code, cardNo, service_id, txt_id):
        url = f'{urls}/api/pay'

        payload = {
            "request_id" : txt_id,
            "serviceID" : service_id,
            "billersCode" : cardNo,
            "variation_code": variation_code,
            "amount" : str(amount),
            "phone":mobile,
            }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, auth=HTTPBasicAuth(username, password), headers=headers, data = json.dumps(payload))

        #print(response.text.encode('utf8'))
        d_dict = json.loads(response.text)
        # print(d_dict)
        f = []
        for j in d_dict:
            airt = d_dict[j]
            airtime = f.append(airt)
        tv_resp = f[1]['transactions']
        return tv_resp

    def powerVerify(self, meterno, service_id, plan):
        url = f'{urls}/api/merchant-verify'

        payload = {
            "billersCode" :meterno ,
            "serviceID" : service_id,
            "type":plan,
            }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, auth=HTTPBasicAuth(username, password), headers=headers, data = json.dumps(payload))

        #print(response.text.encode('utf8'))
        d_dict = json.loads(response.text)
        f = []
        for j in d_dict:
            tv = d_dict[j]
            s_tv = f.append(tv)
        p_resp = f[1]
        # print(p_resp)
        return p_resp

    
    def Buy_Power(self, txt_id, service_id, meterno, plan, amount, mobile):
        url = f'{urls}/api/pay'

        payload = {
            "request_id" : txt_id,
            "serviceID" : service_id,
            "billersCode" :meterno,
            "variation_code":plan,
            "amount" :amount,
            "phone": mobile
            }
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, auth=HTTPBasicAuth(username, password), headers=headers, data = json.dumps(payload))
        #print(response.text.encode('utf8'))
        d_dict = json.loads(response.text)
        f = []
        for j in d_dict:
            po = d_dict[j]
            s_po = f.append(po)
        po_resp = f[1]
        return f