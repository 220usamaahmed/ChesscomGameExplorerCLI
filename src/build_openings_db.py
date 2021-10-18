import os
import json
import io
from tqdm import tqdm
import chess.pgn
import pickle
import sys


MAX_DEPTH = 100

db_white = {'next_moves': {}}
db_black = {'next_moves': {}}


def load_games(username):
    for f in os.listdir(os.path.join('./data', username.lower())):
        data = json.loads(open(f'./data/{username.lower()}/{f}', 'r').read())

        for game_data in data['games']:
            yield game_data


def add_to_db(db, game, result):
    current_node = db

    for i, move in enumerate(game.mainline_moves()):
        if i > MAX_DEPTH: break
        move = str(move)
        if move in current_node['next_moves']:
            current_node['next_moves'][move]['wins'] += 1 if result == 'win' else 0
            current_node['next_moves'][move]['losses'] += 1 if result == 'loss' else 0
            current_node['next_moves'][move]['draws'] += 1 if result == 'draw' else 0
        else:
            current_node['next_moves'][move] = {
                'wins': 1 if result == 'win' else 0,
                'losses': 1 if result == 'loss' else 0,
                'draws': 1 if result == 'draw' else 0,
                'next_moves': {}
            }
        current_node = current_node['next_moves'][move]


def build_openings_db(username):
    load_games(username)
    for game_data in tqdm(load_games(username)):
        game = chess.pgn.read_game(io.StringIO(game_data['pgn']))
        if game_data['white']['username'] == username:
            if game_data['white']['result'] == 'win':
                # I won as white
                add_to_db(db_white, game, 'win')
            elif game_data['black']['result'] == 'win':
                # I lost as white
                add_to_db(db_white, game, 'loss')
            else:
                # I drew as white
                add_to_db(db_white, game, 'draw')
        else:
            if game_data['black']['result'] == 'win':
                # I won as black
                add_to_db(db_black, game, 'win')
            elif game_data['white']['result'] == 'win':
                # I lost as black
                add_to_db(db_black, game, 'loss')
            else:
                # I drew as black
                add_to_db(db_black, game, 'draw')

    if not os.path.exists(os.path.join('./opening_dbs', username)):
        os.mkdir(os.path.join('./opening_dbs', username))

    pickle.dump(db_white, open(f'./opening_dbs/{username}/white', 'wb'))
    pickle.dump(db_black, open(f'./opening_dbs/{username}/black', 'wb'))


def main():
    if len(sys.argv) == 2:
        # TODO: Error handling Check if data exits
        build_openings_db(sys.argv[1])



if __name__ == '__main__': main()