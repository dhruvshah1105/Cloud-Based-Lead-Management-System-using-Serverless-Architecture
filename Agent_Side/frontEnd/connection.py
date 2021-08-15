from flask import Flask, render_template, request
import boto3

app = Flask(__name__)
status=""
@app.route("/")
@app.route("/index.html")
def home():
    return render_template('index.html')

status = ''
@app.route('/',methods=['POST'])
def form_data():
    global status
    status = request.form['status']
    if status == 'Online':
        return render_template('onlineStatus.html')
    else:
        return render_template('index.html')

@app.route('/action',methods=['POST'])
def red():
    global status
    status = request.form['status']
    if status.lower() == "offline":
        return render_template('index.html')
    else:
        return render_template('onlineStatus.html')

@app.route('/online',methods=['GET'])
def redirect():
    global status
    print(status)
    if status == 'Online':
        Num = Queue_Messages()
        if Num != '0':
            return render_template('popUp.html')
        else:
            return render_template('onlineStatus.html')
    else:
        return render_template('index.html')

def Queue_Messages():
    sqs = boto3.client('sqs')
    response_queue_attributes = sqs.get_queue_attributes(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/385806589240/sending_data_to_sqs_queue',
        AttributeNames=[
            'All',
        ],
    )
    # print(f"get_queue_attributes response:{response_queue_attributes}")
    No_of_messages = response_queue_attributes['Attributes']['ApproximateNumberOfMessages']
    # print(f"No_of_messages : {No_of_messages}")
    return No_of_messages

ReceiptHandle = ''
@app.route('/ok')
def ok():
    # Calling the queue and extracting the data from it.
    sqs = boto3.client('sqs')
    sqs_response = sqs.receive_message(
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
    Messages = sqs_response['Messages']
    global ReceiptHandle
    for i in Messages:
        Mobile_no = i['Body']
        ReceiptHandle = i['ReceiptHandle']
    print(f"MObile: {Mobile_no} ReceiptHandle: {ReceiptHandle}")

    # Fetching Data from the database
    dynamodb = boto3.client('dynamodb')
    dynamodb_response = dynamodb.get_item(
        TableName = 'Loan_Customer_Data',
        Key={
            'Mobile_No': {
                'S': Mobile_no
            }
        }
    )
    data = dynamodb_response['Item']

    # extract form-data from data
    # date = data['Date']['S']
    # available = data['Availability']['S']
    address = data['Address']['S']
    email = data['Email_Id']['S']
    gender = data['Gender']['S']
    fname = data['First_Name']['S']
    country = data['Country']['S']
    lname = data['Last_Name']['S']
    loan_type = data['Loan_Type']['S']
    return render_template('userData.html',
                           fname = fname,
                           lname = lname,
                           gender = gender,
                           address = address,
                           country = country,
                           Mobile_no = Mobile_no,
                           email = email,
                           loan_type = loan_type
                        )

@app.route('/home')
def index():
    return render_template('onlineStatus.html')

@app.route('/update_database',methods=['POST'])
def update_database():
    # getting data from form
    fname = request.form['fname']
    lname = request.form['lname']
    gender = request.form['gender']
    address = request.form['address']
    country = request.form['country']
    phone = request.form['phone']
    email = request.form['email']
    loan = request.form['loan_type']
    loan_amount = request.form['loan_amount']
    remarks = request.form['remarks']

    global ReceiptHandle

    # creating the dynamoDB client and updating the data to database
    client = boto3.client('dynamodb')
    response = client.put_item(
        TableName = 'Loan_Customer_Data',
        Item = {
            'Mobile_No': {
                'S': phone
            },
            'Address': {
                'S': address
            },
            'Country': {
                'S': country
            },
            'Email_Id': {
                'S': email
            },
            'First_Name': {
                'S': fname
            },
            'Gender': {
                'S': gender
            },
            'Last_Name': {
                'S': lname
            },
            'Loan_Type': {
                'S': loan
            },
            'Laon_Amount': {
                'S': loan_amount
            },
            'Remarks': {
                'S': remarks
            }
        },
        ReturnValues='NONE'
    )

    sqs = boto3.client('sqs')
    queue_url = '<-----------ENTER YOU QUEUE URL HERE------------>'

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=ReceiptHandle
        )
        return render_template('onlineStatus.html')
    else:
        return response['ResponseMetadata']['HTTPStatuCode']



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
