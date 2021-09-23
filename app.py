from flask import Flask, render_template, request, redirect, jsonify
# from json import dump
import json
from werkzeug.wrappers import response
from Gameboard import Gameboard
import db


app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

game = None

'''
Implement '/' endpoint
Method Type: GET
return: template player1_connect.html and status = "Pick a Color."
Initial Webpage where gameboard is initialized
'''


@app.route('/', methods=['GET'])
def player1_connect():
    global game
    game = Gameboard()
    return render_template("player1_connect.html", status="Pick a Color.")

'''
Helper function that sends to all boards don't modify
'''


@app.route('/autoUpdate', methods=['GET'])
def updateAllBoards():
    try:
        return jsonify(move=game.board, winner=game.game_result,
                       color=game.player1)
    except Exception:
        return jsonify(move="")


'''
Implement '/p1Color' endpoint
Method Type: GET
return: template player1_connect.html and status = <Color picked>
Assign player1 their color
'''


@app.route('/p1Color', methods=['GET'])
def player1_config():
    game.player1=request.args['color']
    if game.player1=="red":
        game.player2="yellow"
    else:
        game.player2="red"
    # game.player1=response.header.color
    return render_template("player1_connect.html", status=game.player1)
    pass


'''
Implement '/p2Join' endpoint
Method Type: GET
return: template p2Join.html and status = <Color picked> or Error
if P1 didn't pick color first

Assign player2 their color
'''


@app.route('/p2Join', methods=['GET'])
def p2Join():
    if game.player1!="":
        status=game.player2
    else:
        status="Error: P1 didn't pick a color"
    
    return render_template("p2Join.html", status=status)
    pass


'''
Implement '/move1' endpoint
Method Type: POST
return: jsonify (move=<CurrentBoard>,
invalid=True or False, winner = <currWinner>)
If move is valid --> invalid = False else invalid = True
If invalid == True, also return reason= <Why Move is Invalid>

Process Player 1's move
'''


@app.route('/move1', methods=['POST'])
def p1_move():

    if game.isWinner(game.player1):
        return jsonify(move=game.board, invalid = True, reason = "You won", winner = game.player1)

    if game.isWinner(game.player2):
        return jsonify(move=game.board, invalid = True, reason = "Player 2 has won", winner = game.player2)

    if game.current_turn=='p2':
        return jsonify(move=game.board, invalid = True, reason = "Player 2's turn", winner = "")

    if game.remaining_moves==0:
        return jsonify(move=game.board, invalid = True, reason = "It is a Draw", winner = "")

    pos=int(json.loads(request.data.decode('UTF-8'))['column'][-1])-1
    if game.positions[pos]==-1:
        return jsonify(move=game.board, invalid = True, reason = "No space left in this column", winner = "")

    game.board[game.positions[pos]][pos]=game.player1
    game.positions[pos]=game.positions[pos]-1
    game.remaining_moves=game.remaining_moves-1
    game.current_turn='p2'
    if game.isWinner(game.player1):
        return jsonify(move=game.board, invalid=False, winner="Winner is : "+game.player1)
    else:
        return jsonify(move=game.board, invalid=False, winner="")
    pass

'''
Same as '/move1' but instead proccess Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():

    if game.isWinner(game.player2):
        return jsonify(move=game.board, invalid = True, reason = "You won", winner = game.player2)

    if game.isWinner(game.player1):
        return jsonify(move=game.board, invalid = True, reason = "Player 1 has won", winner = game.player1)

    if game.current_turn=='p1':
        return jsonify(move=game.board, invalid = True, reason = "Player 1's turn", winner = "")
    if game.remaining_moves==0:
        return jsonify(move=game.board, invalid = True, reason = "It is a Draw", winner = "")

    pos=int(json.loads(request.data.decode('UTF-8'))['column'][-1])-1
    if game.positions[pos]==-1:
        return jsonify(move=game.board, invalid = True, reason = "No space left in this column", winner = "")

    game.board[game.positions[pos]][pos]=game.player2
    game.positions[pos]=game.positions[pos]-1
    game.remaining_moves=game.remaining_moves-1
    game.current_turn='p1'
    if game.isWinner(game.player2):
        return jsonify(move=game.board, invalid=False, winner=game.player2)
    else:
        return jsonify(move=game.board, invalid=False, winner="")
    pass



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
