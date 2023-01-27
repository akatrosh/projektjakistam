from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class BoardGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    players = db.Column(db.Integer)
    rating = db.Column(db.Float)


with app.app_context():
    db.create_all()



@app.route('/edit_game', methods=['POST'])
def edit_game():
    game_id = request.form['game_id']
    game = BoardGame.query.get(game_id)
    game.name = request.form['name']
    game.players = request.form['players']
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/rate_game', methods=['POST'])
def rate_game():
    game_id = request.form['game_id']
    game = BoardGame.query.get(game_id)
    game.rating = request.form['rating']
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        players = request.form['players']
        rating = request.form['rating']
        new_game = BoardGame(name=name, players=players, rating=rating)
        db.session.add(new_game)
        db.session.commit()

    sort_by = request.args.get('sort_by', 'name')
    if sort_by == 'name':
        games = BoardGame.query.order_by(BoardGame.name).all()
    elif sort_by == 'players':
        games = BoardGame.query.order_by(BoardGame.players).all()
    elif sort_by == 'rating':
        games = BoardGame.query.order_by(BoardGame.rating).all()
    else:
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
    app.run(debug=False, port=5000, host='0.0.0.0')