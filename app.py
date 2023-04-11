from flask import Flask, request,jsonify
import requests
import json

app = Flask(__name__)

@app.route('/webhook',methods = ['GET','POST'])
def webhook():

    data = request.get_json(silent=True)
    try:
        if data['queryResult']['intent']['displayName'] == '1.1.1-await-id':
            reply = checkCustID(data)
            return jsonify(reply)
        
        elif data['queryResult']['intent']['displayName'] == '1.2.1-phone-id':
            reply = updatePhone(data)
            return jsonify(reply)
    except Exception as e:
        print('error main: ',e)

def checkCustID(data):
    try:
        id = data['queryResult']['parameters']['id']
        # print(id)
        # print(type(id))
        # new_id = str(id)
        data = requests.get(f'https://sheetdb.io/api/v1/7vcqtbvathyec/search?UniqueRef={id}')
        result = data.json()
        # print(result)
        if len(result):
            record = result[0]
            firstName = record['First Name']
            phone = record['Phone']
            email = record['Email']
            address = record['Address 1']
            quantity = record['Quantity P1']
            print(firstName)
            reply={
                'fulfillmentText': f"We found your record your details are: \nFirst Name: {firstName}\nPhone: {phone}\nEmail: {email}\nAddress: {address}\nQuantity: {quantity}"
            }
        else:
            reply={
                'fulfillmentText': "We didn't found any record against your given id."
            }
    except Exception as e:
        print(e)

    return reply

def updatePhone(data):
    try:
        id = data['queryResult']['parameters']['id']
        phone = data['queryResult']['parameters']['phone']   
        url = f'https://sheet.best/api/sheets/6310829d-6acb-4009-90c2-39fe2cdcbbc3/UniqueRef/{id}'
        payload = json.dumps({
            'Phone':phone
        })
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("PATCH", url, headers=headers, data=payload)
        # print(response.json())
        result = response.json()
        if not result:
            reply={
                'fulfillmentText': "Didn't find this unique id in our database please recheck your id"
            }
        else:
            reply = {
                'fulfillmentText': 'Record Updated Successfully'
            }
    except Exception as e:
        print(e)

    return reply
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
