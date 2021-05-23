from funcs import *

# GET DEX.AG TOKEN LIST
rPair = requests.get("https://api-v2.dex.ag/token-list-full")
tokenList = rPair.json()
tokenList = checksumAddress(tokenList)

i = 0
f = open("arbitrage.txt", "a")
amounts = []

inchProtocolsUrl = 'https://api.1inch.exchange/v3.0/1/protocols'
response = session.get(inchProtocolsUrl)
protocols = (json.loads(response.text))['protocols']

threads = []

for token0 in tokenList:
    token0Amount = int(tokenAmount1inch(token0['address']))
    if (token0Amount == 0):
        token0Amount = AMOUNT_PER_TRADE
    for token1 in tokenList:

        if (token0 == token1):
            continue

        print('\n------------------------------------------\n')
        print('Search arbitrage on {}/{} pair\n'.format(token0['symbol'], token1['symbol']))
        print('Amount to trade : {} {}\n'.format(token0Amount, token0['symbol']))
        amounts.clear()

        i = 0
        while (i < len(protocols) - THREADS - 1):
            nthread = 0
            threads.clear()
            while (nthread < THREADS):
                threads.append(amountThread(token0['address'], token1['address'], token0Amount, protocols[i + nthread], amounts))
                (threads[nthread]).start()
                nthread += 1
            for t in threads:
                t.join()
            i += THREADS

        #pp.pprint(amounts)
        print('\n')
        if (len(amounts) < 2):
            print("Not enough amounts to search an arbitrage, go to the next pair...\n")
            continue

        higher, lower, lower_dex, higher_dex = getBenef(amounts)
        if (higher - lower == 0):
            print("No opportunities found on this pair, go to the next pair...\n")
            continue

        try:
            benef = tokenToUsd(token1['address'], int(higher - lower))
            if (benef == 0):
                raise ValueError("Can't retreive token value in USD")
            print('You can win {} USD on the pair {}/{} between {} and {} !'.format(benef, token0['symbol'], token1['symbol'], lower_dex, higher_dex))
            f.write('You can win {} USD on the pair {}/{} between {} and {} !\n'.format(benef, token0['symbol'], token1['symbol'], lower_dex, higher_dex))
        except:
            print('You can win {} {} on the pair {}/{} between {} and {} !'.format(higher - lower, token1['symbol'], token0['symbol'], token1['symbol'], lower_dex, higher_dex))
            f.write('You can win {} {} on the pair {}/{} between {} and {} !\n'.format(higher - lower, token1['symbol'], token0['symbol'], token1['symbol'], lower_dex, higher_dex))
        time.sleep(5)

f.close()