# Arbitrage bot (1inch API version)

/!\ Project under developpement, not ready for production

## Features

* Get an ERC-20 top tokens list ✅
* Compare prices of pairs between different DEXs through 1inch API ✅
* Call the flash loan and swap smart contract when an opportunitie is found ❌

## Usage

Clone the repo
* `git clone https://github.com/mavileo/Arbitrage_bot -b api`
* `cd Arbitrage_bot`

Install dependancies
* `pip install -r requirements.txt`

Set the number of threads you want in the `THREADS` variable in `consts.py` file
* default : `THREADS = 10`

Run the bot
* `python bot.py`

Fot the moment, the bot will only show you pairs it search arbitrage on and tells you when a profitable arbitrage is found.
It will also save profitables opportinities found in the `arbitrage.txt` file.
