import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from gevent.pywsgi import WSGIServer
import os

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)*100
    
    if(output>100):
        return render_template('index.html', prediction_text='Chance of Admission: 100%')
    if(output<0):
        return render_template('index.html', prediction_text='Chance of Admission: 0%')

    return render_template('index.html', prediction_text='Chance of Admission: {}%'.format(output))
port = os.getenv('VCAP_APP_PORT', '8080')

if __name__ == "__main__":
    app.secret_key=os.urandom(12)
    app.run(debug=True,host='0.0.0.0',port=port)
