from funcs import *

# RETURN N AMOUNT OF TOKEN CORRESPONDING TO THE "AMOUNT_PER_TRADE" VALUE IN USD
def tokenAmount1inch(token0):
    parameters = {
    'fromTokenAddress':daiAddress,
    'toTokenAddress':token0,
    'amount':AMOUNT_PER_TRADE
    }
    response = session.get(inchQuoteUrl, params=parameters)
    try:
        return (json.loads(response.text))['toTokenAmount']
    except:
        return 0

# GET DEX.AG TOKEN LIST
rPair = requests.get("https://api-v2.dex.ag/token-list-full")
tokenList = rPair.json()
tokenList = checksumAddress(tokenList)

# Create web3 object
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Create Uniswap factory contract object
uniFactory = web3.eth.contract(address=uniFactoryAddress, abi=uniFactoryAbi)

# Create Sushiswap factory contract object
sushiFactory = web3.eth.contract(address=sushiFactoryAddress, abi=uniFactoryAbi)

# Create Uniswap router contract object
uniRouter02 = web3.eth.contract(address=uniRouter02Address, abi=uniRouter02Abi)

# Create Sushiswap router contract object
sushiRouter02 = web3.eth.contract(address=sushiRouter02Address, abi=uniRouter02Abi)

# Get Bancor network contract address and create the object
bancorContractRegistry = web3.eth.contract(address=bancorContractRegistryAddress, abi=bancorContractRegistryABI)
bancorNetworkAddress = bancorContractRegistry.functions.addressOf('0x42616e636f724e6574776f726b').call()
bancorNetwork = web3.eth.contract(address=bancorNetworkAddress, abi=bancorNetworkABI)

i = 0
f = open("arbitrage.txt", "a")
amounts = []

for token0 in top10ERC:

    token0Amount = int(tokenAmount1inch(token0['address']))
    if (token0Amount == 0):
        token0Amount = 1

    for token1 in top10ERC:

        if (token0 == token1):
            continue

        print('\n------------------------------------------\n')
        print('Search arbitrage on {}/{} pair\n'.format(token0['symbol'], token1['symbol']))
        amounts.clear()
        path = [token0['address'], token1['address']]
        revPath = [token1['address'], token0['address']]

        print("Amount : {} {}\n".format(token0Amount, token0['symbol']))
        
        # GET THE UNISWAP RATE
        try:
            amountUni = uniRouter02.functions.getAmountsOut(token0Amount, path).call()
            amounts.append(web3.fromWei(amountUni[1], 'microether'))
        except Exception as e:
            amounts.append(-1)
            print("Can't swap the pair {}/{} on Uniswap : {}\n".format(token0['symbol'], token1['symbol'], e))
        
        # GET THE SUSHISWAP RATE
        try:
            amountSushi = sushiRouter02.functions.getAmountsOut(token0Amount, path).call()
            amounts.append(web3.fromWei(amountSushi[1], 'microether'))
        except Exception as e:
            amounts.append(-1)
            print("Can't swap the pair {}/{} on Sushiswap : {}\n".format(token0['symbol'], token1['symbol'], e))

        # GET THE BANCOR RATE
        bancorPath = bancorNetwork.functions.conversionPath(path[0], path[1]).call()
        try:
            amountBancor = bancorNetwork.functions.rateByPath(bancorPath, token0Amount).call()
            amounts.append(web3.fromWei(amountBancor, 'microether')) if amountBancor != 0 else amounts.append(-1)
        except Exception as e:
            amounts.append(-1)
            print("Can't swap the pair {}/{} on Bancor : {}\n".format(token0['symbol'], token1['symbol'], e))

        print("Amounts : {}".format(amounts))

        if (checkAmountsList(amounts) == 0):
            print("Not enough amounts to search an arbitrage...")
            continue

        cheapDex, cheap = findCheapest(amounts)
        expensDex, expens = findExpensivest(amounts)

        if (cheapDex == -1 or expensDex == -1):
            print("Not enough amounts to search an arbitrage...")
            continue

        print("Cheapest rate : {} on {}".format(cheap, dexList[cheapDex]))
        print("Expensivest rate : {} on {}".format(expens, dexList[expensDex]))
        benef = cheap - expens
        if (benef > 0):
            print("You can win {} USD".format(benef))
            print("Token0 : {}\nToken1 : {}\n".format(token0['symbol'], token1['symbol']))
            f.write("{}/{} on {} and {} : {}\n".format(token0['symbol'], token1['symbol'], dexList[cheapDex], dexList[expensDex], benef))
        else:
            print("No profitable arbitrage found on this pair, go to the next token...\n")

f.close()