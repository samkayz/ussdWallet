import requests



urls = 'https://www.bulksmsnigeria.com'
api_token = 'nnShveVAwEpHpQv3O9lYbuXywC6VBNxZZZXTeGQmx4OMfZmHyYPVvLMrUl8O'
mfrom = 'JUST USSD'
class SMS:

    def SendSMS(self, mobile, msg):
        url = f'{urls}/api/v1/sms/create?api_token={api_token}&from={mfrom}&to={mobile}&body={msg}'

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        return response