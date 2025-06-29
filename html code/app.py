from flask import Flask, render_template, request
import pickle
import pandas as pd

model = pickle.load(open('./model.pkl', 'rb'))


app = Flask(__name__,template_folder="./template",static_folder="./static")

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/form')
def form():
    return render_template('fillout.html')

@app.route('/submit', methods=['POST','GET'])
def submit():
    if request.method == 'POST':
        result = request.form
        print(result)
        user_input = {
            'State': result['stateName'],
            'District': result['district'],
            'Crop': result['crop'],
            'Crop_Year': int(result['year']),
            'Season': result['season'],
            'Area': float(result['area'])
        }
        user_input_df = pd.DataFrame([user_input])
        predicted_production = model.predict(user_input_df)
        pred=abs(int(predicted_production[0] / float(result['area'])))
        return render_template('fillout.html',message=pred)

if __name__ == '__main__':
    app.run()