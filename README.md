# Installation
```sh
git clone https://github.com/Gomez0015/InitigritiFetcher
```

# Usage

Add your Bearer token inside config.json 

## Find Bearer Token

![Tutorial](https://raw.githubusercontent.com/Gomez0015/InitigritiFetcher/main/get_token.jpg)

and then you are ready to run!

```sh
python main.py
```

# Options

```
usage: main.py [-h] [-j FILE] [-s SORT_CODEs]

InitigritiFetcher  -  Fetches all the programs and invites from Intigriti

options:
  -h, --help            show this help message and exit
  -j FILE, --json FILE  Save raw output in a json file
  -s SORT_CODE(s), --sort SORT_CODE(s)
                        Sort output using code(s):
                        1: sort by last update
                        2: sort by name
                        3: sort by status
                        4: sort by max bounty
```