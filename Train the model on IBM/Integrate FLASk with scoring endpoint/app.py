import numpy as np
from flask import Flask, request, jsonify, render_template
import requests


@app.route('/predict',methods=['POST'])
def predict():
    if request.method=='POST':
        arr=[]
        for i in request.form:
            val=request.form[i]
            if val=='':
                return redirect(url_for("index"))
            arr.append(float(val))
    API_KEY = "nQEyHT6vwk3OOGrfMn9vhPFBd4vN0ZzQ6o2gcQrJsJqD"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
    API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


    payload_scoring = {"input_data": [{"fields": ['GRE Score',
                                                  'TOEFL Score',
                                                  'CGPA'],
                                       "values": [arr]}]}
    response_scoring = requests.post(
            'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/4b3731ea-275f-476e-8667-fc2b66b5085f/predictions?version=2022-11-18', 
            json=payload_scoring,
            headers=header
        ).json()

    output = round(prediction[0], 2)*100
    
    if(output>100):
        return render_template(url_for, prediction_text='Chance of Admission: 100%')
    if(output<0):
        return render_template(url_for, prediction_text='Chance of Admission: 0%')

    return render_template(url_for', prediction_text='Chance of Admission: {}%'.format(output))
@app.route("/home")
def index():
    return render_template("index.html")   

if __name__ == "__main__":
    app.run()
