# Arbitrage bot

/!\ Project under developpement, not ready for production

## Features

* Get an ERC-20 top tokens list
* Compare prices of pairs between different DEXs
* Call the flash loan and swap smart contract when an opportunitie is found

## Usage

Go to `infura.io`, sign up and retreive you free API key.

Clone the repo
* `git clone https://github.com/mavileo/Arb_bot`
* `cd Arb_bot`

Create a `.env' file and add your API key in it
* `echo "INFURA_KEY=your_key" > .env`

Run the bot
* `source env/bin/activate`
* `python bot.py`

Fot the moment, the bot will only show you pairs it search arbitrage on and tells you when a profitable arbitrage is found.
It will also save profitables opportinities found in the `arbitrage.txt` file.
