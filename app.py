from flask import Flask, render_template, request, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'myman'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
debug = DebugToolbarExtension(app)

@app.route('/')
def home():
    '''show board'''
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore',0)
    num_games = session.get('num_games',0)

    return render_template('index.html',board=board, highscore=highscore,num_games=num_games)

@app.route('/word-check')
def word_check():
    '''check dictionary for word'''
    word = request.args['word']
    board = session['board']
    response = boggle_game.check_valid_word(board,word)

    return jsonify ({'result':response})

@app.route('/show-score', methods=['POST'])
def show_score():
    '''post score/high scores and number of attempts(plays)'''
    score = request.json['score']
    highscore = session.get('highscore',0)
    num_games = session.get('num_games',0)

    session['num_games'] = num_games + 1
    session['highscore'] = max(score,highscore)

    return jsonify(newRecord = score > highscore)