from flask import Flask, render_template, request
import requests
import boto3
import json
import flask

app = Flask(__name__)

@app.route("/")
@app.route("/index.html")
def home():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def form_data():
    status = request.form['status']
    if status == 'Online':
        return render_template('onlineStatus.html')
    else:
        return render_template('index.html')


@app.route('/online',methods=['GET'])
def redirect():
    Num = Queue_Messages()
    if Num != '0':
        return render_template('popUp.html')
    else:
        return render_template('onlineStatus.html')

def Queue_Messages():
    sqs = boto3.client('sqs')
    response_queue_attributes = sqs.get_queue_attributes(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/385806589240/sending_data_to_sqs_queue',
        AttributeNames=[
            'All',
        ],
    )
    print(f"get_queue_attributes response:{response_queue_attributes}")
    No_of_messages = response_queue_attributes['Attributes']['ApproximateNumberOfMessages']
    print(f"No_of_messages : {No_of_messages}")
    return No_of_messages

def Queue_data():
    sqs = boto3.client('sqs')
    response = sqs.receive_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/385806589240/sending_data_to_sqs_queue',
        AttributeNames=[
            'All',
        ],
        MessageAttributeNames=[
            'All',
        ],
        MaxNumberOfMessages=1,
        VisibilityTimeout=600,
        WaitTimeSeconds=0
    )
    print(response)
    Messages = response['Messages']
    for i in Messages:
        Mobile_no = i['Body']
    print(Mobile_no)
    return Mobile_no

def get_data(Mobile_no):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.get_item(
        TableName = 'Loan_Customer_Data',
        Key={
            'Mobile_No': {
                'S': Mobile_no
            }
        }
    )
    return response['Item']


@app.route('/ok')
def ok():
    Mobile_no = Queue_data()
    data = get_data(Mobile_no)
    # extract form-data from data
    date = data['Date']['S']
    available = data['Availability']['S']
    address = data['Address']['S']
    email = data['Email_Id']['S']
    gender = data['Gender']['S']
    fname = data['First_Name']['S']
    country = data['Country']['S']
    lname = data['Last_Name']['S']
    loan_type = data['Loan_Type']['S']
    return render_template('userData.html',Mobile_no = Mobile_no, date = date, available = available, address = address, email = email, gender = gender, fname = fname, country = country, lname = lname, loan_type = loan_type)

@app.route('/home')
def index():
    return render_template('onlineStatus.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
