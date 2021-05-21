# Arbitrage bot

/!\ Project under developpement, not ready for production

## Features

* Get an ERC-20 top tokens list
* Compare prices of pairs between different DEXs
* Call the flash loan and swap smart contract when an opportunitie is found

## Usage

* `git clone https://github.com/mavileo/Arb_bot`
* `cd Arb_bot`
* `pip install -r requirements.txt`
* `source env/bin/activate`
* `python bot.py`

Fot the moment, the bot will only show you pairs it search arbitrage on and tells you when a profitable arbitrage is found.
It will also save profitables opportinities found in the `arbitrage.txt` file.
