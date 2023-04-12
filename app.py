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
        data = requests.get(f'https://sheetdb.io/api/v1/zwq6ocyskcltz/search?UniqueRef={id}')
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
                'fulfillmentText': f"We found your record your details are: \nFirst Name: {firstName}\nPhone: {phone}\nEmail: {email}\nAddress: {address}\nQuantity: {quantity}",
                "fulfillmentMessages": [
                    {
                        "text": {
                        "text": [
                            f"We found your record your details are: \nFirst Name: {firstName}\nPhone: {phone}\nEmail: {email}\nAddress: {address}\nQuantity: {quantity}"
                        ]
                        }
                    },{
                        "text": {
                        "text": [
                            "Please choose from the below options, you will need your unique reference to hand"
                        ]
                        }
                    },
                    {
                        "text": {
                        "text": [
                            "1) Delivery Date Confirmation\n2) Order Details Confirmation\n3) Update Phone Number\n4) Stop"
                        ]
                        }
                    }
                    ],
            }
        else:
            reply={
                'fulfillmentText': "We didn't found any record against your given id.",
                "fulfillmentMessages": [
                    {
                        "text": {
                        "text": [
                           "We didn't found any record against your given id."
                        ]
                        }
                    },{
                        "text": {
                        "text": [
                            "Please choose from the below options, you will need your unique reference to hand"
                        ]
                        }
                    },
                    {
                        "text": {
                        "text": [
                            "1) Delivery Date Confirmation\n2) Order Details Confirmation\n3) Update Phone Number\n4) Stop"
                        ]
                        }
                    }
                    ],
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
                'fulfillmentText': "Didn't find this unique id in our database please recheck your id",
                "fulfillmentMessages": [
                    {
                        "text": {
                        "text": [
                           "Didn't find this unique id in our database please recheck your id"
                        ]
                        }
                    },{
                        "text": {
                        "text": [
                            "Please choose from the below options, you will need your unique reference to hand"
                        ]
                        }
                    },
                    {
                        "text": {
                        "text": [
                            "1) Delivery Date Confirmation\n2) Order Details Confirmation\n3) Update Phone Number\n4) Stop"
                        ]
                        }
                    }
                    ],
            }
        else:
            reply = {
                'fulfillmentText': 'Record Updated Successfully',
                "fulfillmentMessages": [
                    {
                        "text": {
                        "text": [
                            "Record Updated Successfully"
                        ]
                        }
                    },{
                        "text": {
                        "text": [
                            "Please choose from the below options, you will need your unique reference to hand"
                        ]
                        }
                    },
                    {
                        "text": {
                        "text": [
                            "1) Delivery Date Confirmation\n2) Order Details Confirmation\n3) Update Phone Number\n4) Stop"
                        ]
                        }
                    }
                    ],
            }
    except Exception as e:
        print(e)

    return reply

def deliveryDetails(data):
    try:
        id = data['queryResult']['parameters']['id']
        data = requests.get(f'https://sheetdb.io/api/v1/zwq6ocyskcltz/search?UniqueRef={id}')
        result = data.json()
        print("RESULT IS: ",result)
        if len(result):
            record = result[0]
            orderDetails = record['Customer Confirmed Delivery Date']
            print(orderDetails)
            if orderDetails:
                reply={
                    'fulfillmentText': f"Your Order is Booked for {orderDetails}",
                "fulfillmentMessages": [
                    {
                        "text": {
                        "text": [
                            f"Your Order is Booked for {orderDetails}"
                        ]
                        }
                    },
                    {
                        "text": {
                        "text": [
                            "1) Delivery Date Confirmation\n2) Order Details Confirmation\n3) Update Phone Number\n4) Stop"
                        ]
                        }
                    }
                    ],
                }
            else:
                reply={
                    'fulfillmentText': "Your Order Has Not Been Booked For Delivery Yet",
                "fulfillmentMessages": [
                   {
                        "text": {
                        "text": [
                            "Your Order Has Not Been Booked For Delivery Yet"
                        ]
                        }
                    },{
                        "text": {
                        "text": [
                            "Please choose from the below options, you will need your unique reference to hand"
                        ]
                        }
                    },
                    {
                        "text": {
                        "text": [
                            "1) Delivery Date Confirmation\n2) Order Details Confirmation\n3) Update Phone Number\n4) Stop"
                        ]
                        }
                    }
                    ],
                }
        else:
            reply={
                'fulfillmentText': "We didn't found any record against your given id.",
                "fulfillmentMessages": [
                    {
                        "text": {
                        "text": [
                            "We didn't found any record against your given id."
                        ]
                        }
                    },{
                        "text": {
                        "text": [
                            "Please choose from the below options, you will need your unique reference to hand"
                        ]
                        }
                    },
                    {
                        "text": {
                        "text": [
                            "1) Delivery Date Confirmation\n2) Order Details Confirmation\n3) Update Phone Number\n4) Stop"
                        ]
                        }
                    }
                    ],
            }
    except Exception as e:
        print(e)
    return reply

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',port=port)
