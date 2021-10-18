# Chesscom Game Explorer
This tool lets you download your chess.com games and explore your games for free.

## Usage
You need the chess package to use this tool. Use the following command to install it

```
python -m pip install chess
```

There are 3 steps to using this tool.
### Download data
```
python download_games.py <chess.com username>
```

### Build database
```
python build_openings_db.py <chess.com username>
```

### Explore your games
```
python explore_openings_db.py <chess.com username> <white or black>
```

Type the Move to traverse your games as shown in the image below

![Explore games](./images/explore-screenshot.png)