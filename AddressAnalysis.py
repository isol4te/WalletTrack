from utils import OKLink

API_KEY = 'PUT YOUR API KEY HERE'
WEBHOOKURL = 'PUT YOUR WEBHOOK HERE'
oklink = OKLink(API_KEY)
addressess = [
    '0x3d55ccb2a943d88d39dd2e62daf767c69fd0179f'.lower(),
    '0x146ee71e057e6b10efb93aedf631fde6cbaed5e2'.lower(),
    '0xbdb624cd1051f687f116bb0c642330b2abdfcc06'.lower()
]
# Task 1.1
for address in addressess:
    print('Address: {}'.format(address))
    chains = oklink.getActivedChain(address=address)
    
    for c in chains:
        tokens = []
        print('\tChain Full Name:{}\tChain Short Name:{}\tActived'.format(c['chainFullName'], c['chainShortName']))
        chain = c['chainShortName']
        
        # Task 1.2
        # get native balance
        balances = oklink.getNativeBalances(chain=chain,addresses=[address])
        balance = balances[0]
        print('\t\tNative Token Balance: {}'.format(balance['balance']))
        # get ERC20 holdings
        print('\t\tERC20 holdings:')
        idx = 0
        totalPages = 1
        while(idx < int(totalPages)):
            idx += 1
            _, totalPages, tokensBalances = oklink.getTokenBalances(chain=chain, addresses=[address], protocol='token_20', page=idx)
            if not tokensBalances:
                print('\t\t\tNone')
            for tokenBalance in tokensBalances:
                tokens.append(tokenBalance['tokenContractAddress'])
                print('\t\t\tContract address: {}\tBalance:{}'.format(tokenBalance['tokenContractAddress'], tokenBalance['holdingAmount']))
        # get NFT holdings
        print('\t\tNFT holdings:')
        idx = 0
        totalPages = 1
        while(idx < int(totalPages)):
            idx += 1
            _, totalPages, nfts = oklink.getNFTHolding(chain=chain, address=address, protocol='token_721', page=idx)
            if not nfts:
                print('\t\t\tNone')
            for nft in nfts:
                print('\t\t\tName: {}\tContract: {}\tNFT id: {}'.format(nft['token'], nft['tokenContractAddress'], nft['tokenId']))


        # Task 1.3
        # get token stats from token contract address  
        print('\t\tHolding ERC20 Token Info:')
        if not tokens:
            print('\t\t\tNone')
        for token in tokens:
            _, _, ts = oklink.getTokensStats(chain=chain, contract=token)
            if not ts:
                print('\t\t\tNone')
                break
            stats = ts[0]
            if not stats['price']:
                stats['price'] = 0
            if not stats['transactionAmount24h']:
                stats['transactionAmount24h'] = 0
            if not stats['totalMarketCap']:
                stats['totalMarketCap'] = 0
            if float(stats['totalMarketCap']) > 0 : # filter 
                print('\t\t\tERC20 Token ${}'.format(stats['token']))
                print('\t\t\tprice:\t{} USD'.format(stats['price']))
                print('\t\t\tcontract address:\t{}'.format(stats['tokenContractAddress']))
                print('\t\t\t24H trading volume:\t{} USD'.format(stats['transactionAmount24h']))
                print('\t\t\tTotal Market Cap:\t{} USD\n'.format(stats['totalMarketCap']))


        # Task 1.4
        # analysis address
        print('\t\tInteractive address analysis[TOP 5]:')
        interactives = {}
        idx = 0
        totalPages = 1
        while(idx < int(totalPages)):
            idx += 1
            _, totalPages, txs = oklink.getTransactions(chain=chain, address=address, page=idx)
            if totalPages > 200:
                totalPages = 200
            for tx in txs:
                if tx['from'].lower() == address:
                    addr = tx['to']
                if tx['to'].lower() == address:
                    addr = tx['from']
                if addr not in interactives.keys():
                    interactives[addr] = 1
                else:
                    interactives[addr] += 1
        if interactives:
            dic = {}
            dic.update(dict(sorted(interactives.items(), key=lambda x: x[1], reverse=True)[:5]))

            entities = oklink.getAddressesEntity(chain=chain, addresses=dic.keys())
            for addr in dic.keys():
                flag = False
                for entity in entities:
                    if addr.lower() == entity['address'].lower():
                        print('\t\t\tMost interactive address {}, is [{}], interactive {} times'.format(entity['address'], entity['label'], dic[addr]))
                        flag = True
                if not flag:
                    print('\t\t\tMost interactive address {}, with no label, interactive {} times'.format(addr, dic[addr]))
        else:
            print('\t\t\tNone')

# Task 1.5
tokens = [
    '0xdac17f958d2ee523a2206206994597c13d831ec7', # USDT
    '0x514910771af9ca656af840dff83e8264ecf986ca'  # LINK
]
trackIds = oklink.createWebhookTask(chain=chain, event='tokenTransfer', webhookUrl=WEBHOOKURL, trackName='USDTLINKMonitor', addresses=['0x3d55ccb2a943d88d39dd2e62daf767c69fd0179f'.lower()], contracts=tokens)
input('press to delete track')
for trackId in trackIds:
    tId = trackId['trackerId']
    oklink.deleteWebhookTask(tId)

# _, trackers = oklink.getWebhookList()
# for tracker in trackers:
#     oklink.deleteWebhookTask(tracker['trackerId'])