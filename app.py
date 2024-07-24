from flask import Flask, escape, request, render_template
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open("model.pkl", 'rb'))

# Function to convert categorical values to numerical values
def convert_to_numeric(gender, dependents, education, employed, area):
    gender_dict = {'male': 0, 'female': 1}
    dependents_dict = {'0': 0, '1': 1, '2': 2, '3+': 3}
    education_dict = {'not_graduate': 0, 'graduate': 1}
    employed_dict = {'no': 0, 'yes': 1}
    area_dict = {'urban': 0, 'semiurban': 1, 'rural': 2}
    
    return (
        gender_dict.get(gender.lower(), 0),
        dependents_dict.get(dependents, 0),
        education_dict.get(education.lower(), 0),
        employed_dict.get(employed.lower(), 0),
        area_dict.get(area.lower(), 0)
    )

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        print(request)
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])
        credit = float(request.form['credit'])
        area = request.form['area']

        gender, dependents, education, employed, area = convert_to_numeric(gender, dependents, education, employed, area)
        
        totalincomelog = np.log(ApplicantIncome + CoapplicantIncome)
        LoanAmountlog = np.log(LoanAmount)
        Loan_Amount_Termlog = np.log(Loan_Amount_Term)
        
        prediction = model.predict([[gender, dependents, education, employed, totalincomelog, LoanAmountlog, Loan_Amount_Termlog, area]])

        if prediction == 0:
            prediction = "REJECTED"
        else:
            prediction = "ACCEPTED"

        return render_template("predict.html", prediction_text="Your Loan is {}".format(prediction))
    else:
        return render_template("predict.html")

if __name__ == "__main__":
    app.run(debug=True)
