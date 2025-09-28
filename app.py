from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Full model load 
model = joblib.load('full_charges_model.pkl')

# expected features of model
model_features = ['age', 'bmi', 'children', 
                  'sex_male', 'smoker_yes', 
                  'region_northwest', 'region_southeast', 'region_southwest']

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        # User input 
        age = int(request.form['age'])
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])
        sex = request.form['sex']
        smoker = request.form['smoker']
        region = request.form['region']

        # Encode categorical variables
        sex_male = 1 if sex=='male' else 0
        smoker_yes = 1 if smoker=='yes' else 0
        region_northwest = 1 if region=='northwest' else 0
        region_southeast = 1 if region=='southeast' else 0
        region_southwest = 1 if region=='southwest' else 0
        # northeast is baseline → 0

        # Input DataFrame 
        input_df = pd.DataFrame([[age, bmi, children, sex_male, smoker_yes,
                                  region_northwest, region_southeast, region_southwest]],
                                columns=model_features)

        # Prediction
        prediction = round(model.predict(input_df)[0], 2)

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
