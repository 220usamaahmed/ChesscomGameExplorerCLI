import urllib.request
import json
from tqdm import tqdm
import os
import sys


def download_games(username, storage_dir):
    link = f'https://api.chess.com/pub/player/{username}/games/archives'
    try:
        with urllib.request.urlopen(link) as url:
            data = json.loads(url.read().decode())
            archive_links = data['archives']

        for archive_link in tqdm(archive_links):
            with urllib.request.urlopen(archive_link) as url:
                data = url.read().decode()
                filename = f'archive-{"-".join(archive_link.split("/")[-2:])}'
                with open(f'{storage_dir}/{username}/{filename}.json', 'w') as f:
                    f.write(data)
    except urllib.error.HTTPError as exception:
        print(exception)
        print("Check if your username is correct.")
        

def main():
    if len(sys.argv) == 2:
        username = sys.argv[1]
        if not os.path.exists(os.path.join('./data', username)):
            os.mkdir(os.path.join('./data', username))
        download_games(sys.argv[1], './data')


if __name__ == '__main__': main()