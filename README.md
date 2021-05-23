# Arbitrage bot

/!\ Project under developpement, not ready for production

## Features

* Get an ERC-20 top tokens list
* Compare prices of pairs between different DEXs
* Call the flash loan and swap smart contract when an opportunitie is found

## Usage

Go to `infura.io`, sign up and retreive you free API key.
Go to `etherscan.io`, sign up and retreive you free API key.

Clone the repo
* `git clone https://github.com/mavileo/Arbitrage_bot`
* `cd Arbitrage_bot`

Create a `.env' file and add your API keys in it
* `echo "INFURA_KEY=your_infura_key" > .env`
* `echo "ETHERSCAN_KEY=your_etherscan_key" >> .env`

Install dependancies
* `pip install -r requirements.txt`

Run the bot
* `python bot.py`

Fot the moment, the bot will only show you pairs it search arbitrage on and tells you when a profitable arbitrage is found.
It will also save profitables opportinities found in the `arbitrage.txt` file.
