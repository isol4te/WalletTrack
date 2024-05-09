import requests
import json
BASE_URL = 'https://www.oklink.com'


class OKLink:
    def __init__(self, API_KEY) -> None:
        self.apiKey = API_KEY
        self.hearders = {'Ok-Access-Key':self.apiKey}

    def getActivedChain(self, address):
        url = BASE_URL + '/api/v5/explorer/address/address-active-chain'
        params = {'address':address}
        result = requests.get(url=url, params=params, headers=self.hearders).json()
        if result['code'] == '0':
            return result['data']
        
    def getAddressSummary(self, chain, address):
        url = BASE_URL + '/api/v5/explorer/address/address-summary'
        params = {
            'chainShortName':chain,
            'address':address
        }
        result = requests.get(url=url, params=params, headers=self.hearders).json()
        if result['code'] == '0':
            return result['data'][0]
        
    def getAddressesEntity(self, chain, addresses):
        url = BASE_URL + '/api/v5/explorer/address/entity-label'
        params = {
            'chainShortName':chain,
            'address':addresses
        }
        result = requests.get(url=url, params=params, headers=self.hearders).json()
        if result['code'] == '0':
            return result['data']
    
    # protocols = ['token_20', 'token_721']
    def getTokenBalances(self, chain, addresses, protocol, page=1, limit=50):
        url = BASE_URL + '/api/v5/explorer/address/token-balance-multi'
        params = {
            'chainShortName':chain,
            'address':addresses,
            'protocolType': protocol,
            'limit':limit,
            'page':page
        }

        result = requests.get(url=url, params=params, headers=self.hearders).json()
        if result['code'] == '0':
            currentPage = int(result['data'][0]['page'])
            totalPage = int(result['data'][0]['totalPage'])
            balances = result['data'][0]['balanceList']
            return currentPage, totalPage, balances
        return None, None, None
    
    def getNativeBalances(self, chain, addresses):
        url = BASE_URL + '/api/v5/explorer/address/balance-multi'
        params = {
            'chainShortName':chain,
            'address':addresses,
        }
        result = requests.get(url=url, params=params, headers=self.hearders).json()
        if result['code'] == '0':
            return result['data'][0]['balanceList']
        
    def getTransactions(self, chain, address, protocol='transaction', page=1, limit=50):
        url = BASE_URL + '/api/v5/explorer/address/transaction-list'
        params = {
            'chainShortName':chain,
            'address':address,
            'protocolType': protocol,
            'limit':limit,
            'page':page
        }
        result = requests.get(url=url, params=params, headers=self.hearders).json()
        if result['code'] == '0':
            currentPage = int(result['data'][0]['page'])
            if result['data'][0]['totalPage']:
                totalPage = int(result['data'][0]['totalPage'])
            else:
                totalPage = 0
            txs = result['data'][0]['transactionLists']
            return currentPage, totalPage, txs
        else:
            return None, None, None

    # event: tokenTransfer, nativeTokenTransfer
    def createWebhookTask(self, event, chain, webhookUrl, trackName, addresses, contracts=None, amount=None, valueUSD=None):
        url = BASE_URL + '/api/v5/explorer/webhook/create-address-activity-tracker'
        data = {
            'event':event,
            'chainShortName':chain,
            'webhookUrl':webhookUrl,
            'trackerName':trackName,
            'addresses':addresses,
        }
        if contracts:
            data['tokenContractAddress'] = contracts
        if amount:
            data['amountFilter'] = amount
        if valueUSD:
            data['valueUsdFilter'] = valueUSD

        headers = self.hearders
        headers['Content-Type'] = 'application/json'

        result = requests.post(url=url, data=json.dumps(data), headers=headers).json()
        if result['code'] == '0':
            return result['data']
    
    def getNFTHolding(self, chain, address, protocol='token_721', limit=100, page=0):
        url = BASE_URL + '/api/v5/explorer/nft/address-balance-fills'
        params = {
            'chainShortName': chain,
            'address': address,
            'protocolType':protocol,
            'limit':limit,
            'page':page
        }
        result = requests.get(url=url, params=params, headers=self.hearders).json()
        if result['code'] == '0':
            currentPage = int(result['data'][0]['page'])
            totalPage = int(result['data'][0]['totalPage'])
            nfts = result['data'][0]['tokenList']
            return currentPage, totalPage, nfts
        else:
            return None, None, None
    
    def getWebhookList(self, limit=20, page=0):
        url = BASE_URL + '/api/v5/explorer/webhook/get-tracker-list'
        params = {
            'limit':limit,
            'page':page
        }
        result = requests.get(url=url, params=params, headers=self.hearders).json()
        if result['code'] == '0':
            currentPage = int(result['data'][0]['page'])
            totalPage = int(result['data'][0]['totalPage'])
            trackers = result['data'][0]['trackerList']
            return currentPage, totalPage, trackers
        else:
            return None, None, None

    
    def deleteWebhookTask(self, trackId):
        url = BASE_URL + '/api/v5/explorer/webhook/delete-tracker'
        data = {
            'trackerId':trackId
        }

        headers = self.hearders
        headers['Content-Type'] = 'application/json'

        result = requests.post(url=url, data=json.dumps(data), headers=headers).json()
        if result['code'] == '0':
            return True
    
    def getTokensStats(self, chain, protocol=None, contract=None, start=None, end=None, orderBy=None, page=1, limit=50):
        url = BASE_URL + '/api/v5/explorer/token/token-list'
        params = {
            'chainShortName':chain,
            'limit':limit
        }
        if protocol:
            params['protocolType'] = protocol
        if contract:
            params['tokenContractAddress']=contract
        if start:
            params['startTime'] = start
        if end:
            params['endTime'] = end
        if orderBy:
            params['orderBy'] = orderBy
        if page:
            params['page'] = page

        result = requests.get(url=url, params=params, headers=self.hearders).json()
        if result['code'] == '0':
            currentPage = int(result['data'][0]['page'])
            totalPage = int(result['data'][0]['totalPage'])
            tokens = result['data'][0]['tokenList']
            return currentPage, totalPage, tokens
        else: 
            return None, None, None