from consts import *

# GET THE ABI OF THE CONTRACT PASSED IN ARGS FROM ETHERSCAN
def getAbi(address):
    requestAbi = "https://api.etherscan.io/api?module=contract&action=getabi&address={}&apikey=EWAWKJG96Y9NWG2G5BPHSF5QWI1A3B42R1".format(address)
    r = requests.get(requestAbi)
    data = r.json()
    return data['result']

# montant return != montant uniswap mais coherent (monte qd rate pair monte), formule trouvee ici : https://ethereum.stackexchange.com/questions/91441/how-can-you-get-the-price-of-token-on-uniswap-using-solidity
def getSwapRate(pair, amountIn, pairDecimals):
    res = pair.functions.getReserves().call()
    res[0] = res[0] * (pow(10, pairDecimals))
    return (amountIn * res[0]) / res[1]

# RETURN THE VALUE OF N TOKENS IN USD
def getBenef(token, amount):
    usdtPath = [token, usdtAddress]
    usdcPath = [token, usdcAddress]
    daiPath = [token, daiAddress]
    try:
        benef = sushiRouter02.functions.getAmountsOut(amount, usdtPath).call()
    except:
        try:
            benef = sushiRouter02.functions.getAmountsOut(amount, usdcPath).call()
        except:
            try:
                benef = sushiRouter02.functions.getAmountsOut(amount, daiPath).call()
            except:
                benef = [-1, -1]
    return benef[1]

# GET A STABLECOIN AVAILABLE AS UNISWAP PAIR BETWEEN IT AND THE TOKEN PASSED
def getStablePair(token):
    pairAddress = uniFactory.functions.getPair(token, usdtAddress).call()
    if (pairAddress != '0x0000000000000000000000000000000000000000'):
        return usdtAddress
    pairAddress = uniFactory.functions.getPair(token, usdcAddress).call()
    if (pairAddress != '0x0000000000000000000000000000000000000000'):
        return usdcAddress
    pairAddress = uniFactory.functions.getPair(token, daiAddress).call()
    if (pairAddress != '0x0000000000000000000000000000000000000000'):
        return daiAddress
    return '0x0000000000000000000000000000000000000000'

# RETURN 0x0 IF THE TOKEN WAS ALREADY TESTED
def checkToken(token, tokensTested):
    for i in tokensTested:
        if (i == token):
            return '0x0000000000000000000000000000000000000000'
    return token

def checksumAddress(tokenList):
    for i in tokenList:
        i['address'] = Web3.toChecksumAddress(i['address'])
    return tokenList

def findExpensivest(amounts):
    lower = 999999999999
    ret = -1
    for index, value in enumerate(amounts):
        if (value > 0 and value < lower):
            lower = value
            ret = index
    return (ret, lower) if lower != math.inf else (-1, -1)

def findCheapest(amounts):
    higher = -1
    ret = -1
    for index, value in enumerate(amounts):
        if (value > 0 and value > higher):
            higher = value
            ret = index
    return (ret, higher) if higher > 0 else (-1, -1)

# CHECK IF THERE IS AT LEAST 2 VALIDS AMOUNTS IN THE LIST
def checkAmountsList(amounts):
    valids = 0
    for i in amounts:
        if (i != -1):
            valids += 1
    return 0 if valids < 2 else 1
