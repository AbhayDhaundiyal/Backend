import flask
import pandas as pd
from flask import render_template, request
from sqlalchemy import create_engine

engine = create_engine('sqlite:///task.db')
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/read', methods=['GET', 'POST'])
def insert():
    if request.method == 'GET':
        return "Hello"
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_excel(file)
        for dt in df['volume']:
            v = int(dt) * 100
            if v != dt * 100:
                return "mismatch volume"
        if df['datetime'].dtype != 'datetime64[ns]':
            return "mismatch date" 
        for dt in df['instrument']:
            if type(dt) != str:
                return "mismatch instrument"
        df.astype({'volume' : int, 'close' : float, 'open' : float, 'high' : float, 'instrument' : str})
        df.to_sql(file.filename, con=engine, if_exists='append')
        return 'Sucess !'
if __name__ == '__main__':
	app.run(debug=True)
