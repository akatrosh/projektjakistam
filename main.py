from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

engine = create_engine('sqlite:///test.db')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class ClickCounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    button1_clicks = db.Column(db.Integer, default=0)
    button2_clicks = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()
    default_counter = ClickCounter(button1_clicks=0, button2_clicks=0)
    db.session.add(default_counter)
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        button = request.form['button']
        if button == 'button1':
            counter = ClickCounter.query.first()
            counter.button1_clicks += 1
            db.session.commit()
        elif button == 'button2':
            counter = ClickCounter.query.first()
            counter.button2_clicks += 1
            db.session.commit()
    counter = ClickCounter.query.first()
    return render_template('index.html', button1_clicks=counter.button1_clicks, button2_clicks=counter.button2_clicks)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
