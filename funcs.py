from consts import *

# GET THE ABI OF THE CONTRACT PASSED IN ARGS FROM ETHERSCAN
def getAbi(address):
    requestAbi = "https://api.etherscan.io/api?module=contract&action=getabi&address={}&apikey={}".format(address, ETHERSCAN_KEY)
    r = requests.get(requestAbi)
    data = r.json()
    return data['result']

def getBenef(amounts):
    lower = 99999999999999
    higher = -1
    lower_dex = ''
    higher_dex = ''
    for a in amounts:
        if (a['amount'] < lower and a['amount'] != 0):
            lower = a['amount']
            lower_dex = a['protocol']
        if (a['amount'] > higher and a['amount'] != 0):
            higher = a['amount']
            higher_dex = a['protocol']
    return (higher, lower, lower_dex, higher_dex)

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

def isProtocolNew(amounts, protocol):
    for a in amounts:
        if (a['protocol'] == protocol):
            return False
    return True

# RETURN N AMOUNT OF TOKEN CORRESPONDING TO THE "AMOUNT_PER_TRADE" VALUE IN USD
def tokenAmount1inch(token0):
    parameters = {
    'fromTokenAddress':usdtAddress,
    'toTokenAddress':token0,
    'amount':AMOUNT_PER_TRADE
    }
    response = session.get(inchQuoteUrl, params=parameters)
    inch = json.loads(response.text)
    amount = float(inch['toTokenAmount']) / pow(10, inch['toToken']['decimals'] - inch['fromToken']['decimals'])
    if (amount > 0 and amount < 1):
        return 1
    return amount

def tokenToUsd(token, amount):
    parameters = {
    'fromTokenAddress':token,
    'toTokenAddress':usdtAddress,
    'amount':amount
    }
    response = session.get(inchQuoteUrl, params=parameters)
    inch = json.loads(response.text)
    try:
        return int(inch['toTokenAmount']) / pow(10, inch['fromToken']['decimals'] - inch['toToken']['decimals'])
    except:
        print('FAIL TO GET THE USD PRICE')
        return -1

# Get the amount from token0 to token1 from 1inch Quote API
threadLockPrint = threading.Lock()
threadLock = threading.Lock()
def getAmount(token0, token1, amount, protocol, amounts):
    parameters = {
    'fromTokenAddress':token0,
    'toTokenAddress':token1,
    'amount':amount,
    'protocol':protocol
    }
    response = session.get(inchQuoteUrl, params=parameters)
    inch = json.loads(response.text)
    #pp.pprint(inch)
    try:
        retAmount = float(inch['toTokenAmount']) / pow(10, inch['toToken']['decimals'] - inch['fromToken']['decimals'])
    except:
        return -1
    threadLockPrint.acquire()
    print('{} protocol : {}'.format(protocol, retAmount))
    threadLockPrint.release()
    
    if (inch['protocols'] == [] or retAmount == 0):
        return -1
    # incoherents results when CURVE protocol is present, idk why for the moment so skip if it is present
    for l in inch['protocols'][0]:
        for p in l:
            if (p['name'] == 'CURVE'):
                return -1
    threadLock.acquire()
    amounts.append({'protocol': protocol, 'amount': retAmount})
    threadLock.release()

class amountThread (threading.Thread):
   def __init__(self, token0, token1, amount, protocol, amounts):
      threading.Thread.__init__(self)
      self.token0 = token0
      self.token1 = token1
      self.amount = amount
      self.protocol = protocol
      self.amounts = amounts
   def run(self):
      getAmount(self.token0, self.token1, self.amount, self.protocol, self.amounts)
