import pickle
import sys


def explore_openings_db(username, color):
    db = pickle.load(open(f'./opening_dbs/{username}/{color}', 'rb'))
    current_node = db

    i = 0
    while True:
        print("#\tMOVE\tTOTAL\tWINS\tDRAWS\tLOSSES\tPERCENTAGE")
        print('_'*68)
        print()
        moves = []
        for move in current_node['next_moves']:
            moves.append((move, 
                current_node['next_moves'][move]['wins'],
                current_node['next_moves'][move]['draws'],
                current_node['next_moves'][move]['losses']))
            
        for i, (move, wins, draws, losses) in enumerate(sorted(moves, key=lambda x: sum(x[1:]), reverse=True)):
            total = wins + draws + losses
            win_bar = '\033[92m█' * int(wins * 20 / total)
            loss_bar = '\033[91m█' * int(losses * 20 / total)
            draw_bar = '\033[93m█' * (20 - int(wins * 20 / total) - int(losses * 20 / total))
            percent_bar = win_bar + draw_bar + loss_bar + '\033[0m'
            print(f'{i}\t{move}\t{total}\t{wins}\t{draws}\t{losses}\t{percent_bar}')
        print("\n\n")

        if i % 2 == 0:
            move = input('Enter white\'s move or q to quit: ')      
        else:
            move = input('Enter black\'s move or q to quit: ')

        if move == 'q':
            break
            
        if not move in current_node['next_moves']:
            print("This move was not played in any game.")
        else:
            current_node = current_node['next_moves'][move]
            

def main():
    if len(sys.argv) == 3:
        if (color := sys.argv[2]) in ('white', 'black'):
            explore_openings_db(sys.argv[1], color)


if __name__ == '__main__':
    main()