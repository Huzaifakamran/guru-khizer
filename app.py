from flask import Flask, request,jsonify
import requests
import json
import os
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
        
        elif data['queryResult']['intent']['displayName'] == '1.3.1-await-delivery-id':
            reply = deliveryDetails(data)
            return jsonify(reply)
        
    except Exception as e:
        print('error main: ',e)

def checkCustID(data):
    try:
        id = data['queryResult']['parameters']['id']
        data = requests.get(f'https://sheetdb.io/api/v1/<api-key>/search?UniqueRef={id}')
        result = data.json()
        print("RESULT IS: ",result)
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
        url = f'https://sheet.best/api/sheets/<api-key>/UniqueRef/{id}'
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

def deliveryDetails(data):
    try:
        id = data['queryResult']['parameters']['id']
        data = requests.get(f'https://sheetdb.io/api/v1/<api-key>/search?UniqueRef={id}')
        result = data.json()
        print("RESULT IS: ",result)
        if len(result):
            record = result[0]
            orderDetails = record['Customer Confirmed Delivery Date']
            print(orderDetails)
            if orderDetails:
                reply={
                    'fulfillmentText': f"Your Order is Booked for {orderDetails}"
                }
            else:
                reply={
                    'fulfillmentText': "Your Order Has Not Been Booked For Delivery Yet"
                }
        else:
            reply={
                'fulfillmentText': "We didn't found any record against your given id."
            }
    except Exception as e:
        print(e)
    return reply

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',port=port)
