from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
@app.route("/index.html")
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def form_data():
    fname = request.form['fname']
    lname = request.form['lname']
    gender = request.form['gender']
    address = request.form['address']
    country = request.form['country']
    phone = request.form['phone']
    email = request.form['email']
    loan = request.form['loan']
    rdbutton = request.form['rdbutton']
    if rdbutton == 'Disable':
        date = ''
    elif rdbutton == 'Enable':
        date = request.form['date']

    API_ENDPOINT = '<------------ENTER YOUR API----------->'

    data = {'First_Name': fname,
            'Last_Name': lname,
            'Gender': gender,
            'Address': address,
            'Country': country,
            'Mobile_No': phone,
            'Email_Id': email,
            'Loan_Type': loan,
            'Availability': rdbutton,
            'Date': date
    }

    response = requests.post(url = API_ENDPOINT, json = data)
    return response.text

if __name__ == "__main__":
    app.run(debug=True)
