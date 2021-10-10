from flask import Flask, render_template, request, jsonify
# from json import dump
import json
from Gameboard import Gameboard
import logging
import db
import ast

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
game = Gameboard()

'''
Implement '/' endpoint
Method Type: GET
return: template player1_connect.html and status = "Pick a Color."
Initial Webpage where gameboard is initialized
'''


@app.route('/', methods=['GET'])
def player1_connect():
    db.clear()
    db.init_db()
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
    move = db.getMove()
    if move is not None:
        board = list(ast.literal_eval(move[1]))
        print(board)
        game.player1 = move[3]
        game.player2 = move[4]
        game.board = board
        game.game_result = move[2]
        for i in range(len(board[0])):
            col = 0
            for j in range(len(board)):
                if board[j][i] != 0:
                    col += 1
            game.positions[i] = 5-col
        game.current_turn = move[0]
        game.remaining_moves = move[5]
        return render_template("player1_connect.html", status=game.player1)
    color = request.args.get('color')
    game.player1 = color
    if game.player1 == "red":
        game.player2 = "yellow"
    else:
        game.player2 = "red"
    # if game.player1 == "" or game.player2 == "":
    #     game.player1 = request.args['color']
    #     if game.player1 == "red":
    #         game.player2 = "yellow"
    #     else:
    #         game.player2 = "red"
    return render_template("player1_connect.html", status=color)
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

    move = db.getMove()
    print("This is p2join")
    print(move)
    if move is not None:
        board = list(ast.literal_eval(move[1]))
        print(board)
        game.player1 = move[3]
        game.player2 = move[4]
        game.board = board
        game.game_result = move[2]
        game.current_turn = move[0]
        for i in range(len(board[0])):
            col = 0
            for j in range(len(board)):
                if board[j][i] != 0:
                    col += 1
            game.positions[i] = 5-col

        game.remaining_moves = move[5]
        # return render_template("p2Join.html", status=game.player2)
    if game.player1 == "":
        return render_template("p2Join.html",
                               status="Error: P1 didn't pick a color")
    return render_template("p2Join.html", status=game.player2)

    # db.getMove()
    # if game.player1 == "":
    #     status = "Error: P1 didn't pick a color"
    #     return render_template("p2Join.html", status=status)
    # elif game.player1 == "red":
    #     game.player2 = "yellow"
    #     return render_template("p2Join.html", status="yellow")
    # else:
    #     game.player2 = "red"
    #     return render_template("p2Join.html", status="red")
    # if game.player1 == "":
    #     status = game.player2
    # else:
    #     status = "Error: P1 didn't pick a color"
    # return render_template("p2Join.html", status=status)
    # pass


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

    if game.winnerDeclared():
        return jsonify(move=game.board, invalid=True, reason="You won",
                       winner=game.game_result)

    if not game.players_turn('p1'):
        return jsonify(move=game.board, invalid=True, reason="Player 2's turn",
                       winner="")

    if game.isDraw():
        return jsonify(move=game.board, invalid=True, reason="It is a Draw",
                       winner="")

    pos = int(json.loads(request.data.decode('UTF-8'))['column'][-1])-1
    print(pos)
    if game.isCurrentColumnFilled(pos):
        return jsonify(move=game.board, invalid=True,
                       reason="No space left in this column", winner="")

    game.happyMove('p1', pos)

    if game.isWinner('p1'):
        return jsonify(move=game.board, invalid=False,
                       winner="Winner is: " + game.player1)
    else:
        return jsonify(move=game.board, invalid=False, winner="")


'''
Same as '/move1' but instead proccess Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():

    if game.winnerDeclared():
        return jsonify(move=game.board, invalid=True, reason="You won",
                       winner=game.game_result)

    if not game.players_turn('p2'):
        return jsonify(move=game.board, invalid=True, reason="Player 1's turn",
                       winner="")

    if game.isDraw():
        return jsonify(move=game.board, invalid=True, reason="It is a Draw",
                       winner="")

    pos = int(json.loads(request.data.decode('UTF-8'))['column'][-1])-1
    if game.isCurrentColumnFilled(pos):
        return jsonify(move=game.board, invalid=True,
                       reason="No space left in this column", winner="")

    game.happyMove('p2', pos)

    if game.isWinner('p2'):
        return jsonify(move=game.board, invalid=False, winner=game.player2)
    else:
        return jsonify(move=game.board, invalid=False, winner="")


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
