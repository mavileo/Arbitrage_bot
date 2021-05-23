import requests, json, pprint, math, os
from web3 import Web3
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from coinmarketcapapi import CoinMarketCapAPI
from dotenv import load_dotenv

AMOUNT_PER_TRADE = 1000

load_dotenv()

INFURA_KEY = os.getenv('INFURA_KEY')
ETHERSCAN_KEY = os.getenv('ETHERSCAN_KEY')

# Create PrettyPrint obj
pp = pprint.PrettyPrinter(indent=4)

# Create Requests session
session = Session()

# 1inch Quote API URL
inchQuoteUrl = 'https://api.1inch.exchange/v3.0/1/quote'

INFURA_URL = "https://mainnet.infura.io/v3/{}".format(INFURA_KEY)

dexList = ['Uniswap', 'Sushiswap', 'Bancor']

# DEX contracts address
uniFactoryAddress = Web3.toChecksumAddress("0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f")
uniRouter02Address = Web3.toChecksumAddress("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")

sushiFactoryAddress = Web3.toChecksumAddress("0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac")
sushiRouter02Address = Web3.toChecksumAddress("0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F")

pancakeFactoryAddress = Web3.toChecksumAddress("0xbcfccbde45ce874adcb698cc183debcf17952812")
pancakeRouter02Address = Web3.toChecksumAddress("0x10ED43C718714eb63d5aA57B78B54704E256024E")

bancorContractRegistryAddress = Web3.toChecksumAddress("0x52Ae12ABe5D8BD778BD5397F99cA900624CfADD4")

# ERC20 tokens
wethAddress = Web3.toChecksumAddress("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
daiAddress = Web3.toChecksumAddress("0x6b175474e89094c44da98b954eedeac495271d0f")
bnbAddress = Web3.toChecksumAddress("0xB8c77482e45F1F44dE1745F52C74426C631bDD52")
usdtAddress = Web3.toChecksumAddress("0xdac17f958d2ee523a2206206994597c13d831ec7")
usdcAddress = Web3.toChecksumAddress("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
uniAddress = Web3.toChecksumAddress("0x1f9840a85d5af5bf1d1762f925bdaddc4201f984")
shibAddress = Web3.toChecksumAddress("0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE") # LOW MC SHITCOIN
bzntAddress = Web3.toChecksumAddress("0xe1aee98495365fc179699c1bb3e761fa716bee62") # LOW MC SHITCOIN
nrpAddress = Web3.toChecksumAddress("0x3918c42f14f2eb1168365f911f63e540e5a306b5") # LOW MC SHITCOIN
kndcAddress = Web3.toChecksumAddress("0x8e5610ab5e39d26828167640ea29823fe1dd5843") # LOW MC SHITCOIN
bynAddress = Web3.toChecksumAddress("0x4Bb3205bf648B7F59EF90Dee0F1B62F6116Bc7ca") # LOW MC SHITCOIN
truAddress = Web3.toChecksumAddress("0xf65B5C5104c4faFD4b709d9D60a185eAE063276c")
maticAddress = Web3.toChecksumAddress("0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0")
udtAddress = Web3.toChecksumAddress("0x90DE74265a416e1393A450752175AED98fe11517")
hexAddress = Web3.toChecksumAddress("0x2b591e99afE9f32eAA6214f7B7629768c40Eeb39")

top10ERC = [{'address':Web3.toChecksumAddress('0xB8c77482e45F1F44dE1745F52C74426C631bDD52'),
            'symbol':'BNB'},
            {'address':Web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7'),
            'symbol':'USDT'},
            {'address':Web3.toChecksumAddress('0x1f9840a85d5af5bf1d1762f925bdaddc4201f984'),
            'symbol':'UNI'},
            {'address':Web3.toChecksumAddress('0x514910771af9ca656af840dff83e8264ecf986ca'),
            'symbol':'LINK'},
            {'address':Web3.toChecksumAddress('0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'),
            'symbol':'USDC'},
            {'address':Web3.toChecksumAddress('0xd850942ef8811f2a866692a623011bde52a462c1'),
            'symbol':'VEN'},
            {'address':Web3.toChecksumAddress('0x2b591e99afe9f32eaa6214f7b7629768c40eeb39'),
            'symbol':'HEX'},
            {'address':Web3.toChecksumAddress('0x3883f5e181fccaf8410fa61e12b59bad963fb645'),
            'symbol':'THETA'},
            {'address':Web3.toChecksumAddress('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'),
            'symbol':'WETH'},
            {'address':Web3.toChecksumAddress('0x2260fac5e5542a773aa44fbcfedf7c193bc2c599'),
            'symbol':'WBTC'}]

# GET IUniswapV2Factory ABI
rFactory = requests.get("https://unpkg.com/@uniswap/v2-core@1.0.0/build/IUniswapV2Factory.json")
tmp = rFactory.json()
uniFactoryAbi = tmp['abi']

# GET IUniswapV2Pair ABI
rPair = requests.get("https://unpkg.com/@uniswap/v2-core@1.0.0/build/IUniswapV2Pair.json")
tmp = rPair.json()
uniPairAbi = tmp['abi']

# GET IUniswapV2Router02 ABI
rRouter02 = requests.get("https://unpkg.com/@uniswap/v2-periphery@1.1.0-beta.0/build/IUniswapV2Router02.json")
tmp = rRouter02.json()
uniRouter02Abi = tmp['abi']

# GET Bancor ContractRegistry ABI
rContractRegistry = requests.get("https://raw.githubusercontent.com/bancorprotocol/docs/master/ethereum-contracts/build/ContractRegistry.abi")
bancorContractRegistryABI = rContractRegistry.json()

# GET Bancor Network ABI
rNetwork = requests.get("https://raw.githubusercontent.com/bancorprotocol/docs/master/ethereum-contracts/build/BancorNetwork.abi")
bancorNetworkABI = rNetwork.json()

