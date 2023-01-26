from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class BoardGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    players = db.Column(db.Integer)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        players = request.form['players']
        new_game = BoardGame(name=name, players=players)
        db.session.add(new_game)
        db.session.commit()
    games = BoardGame.query.all()
    return render_template('index.html', games=games)
@app.route('/delete_game', methods=['POST'])
def delete_game():
    game_id = request.form['game_id']
    game = BoardGame.query.get(game_id)
    db.session.delete(game)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')