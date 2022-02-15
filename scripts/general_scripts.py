from brownie import network, accounts, config, Contract, MockDAI, MockWETH, MockV3Aggregator


DECIMALS = 8
STARTING_VALUE = 2000


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    elif id:
        return accounts.load(id)
    elif not config['networks'][network.show_active()]['local'] is False:
        return accounts[0]
    else:
        return accounts.add(config['wallets']['dev_account_1']['private_key'])

contracts_to_mock = {'eth_usd_price_feed': MockV3Aggregator,
                     'dai_usd_price_feed': MockV3Aggregator,
                     'weth_token': MockWETH,
                     'fau_token': MockDAI}

def get_contract(contract_name):
    contract_type = contracts_to_mock[contract_name]
    if config['networks'][network.show_active()]['local'] is True:
        deploy_mocks(contract_type)
        contract = contract_type[-1]
    
    else:
        contract_address = config['networks'][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)

    return contract

def deploy_mocks( contract_type, decimals=DECIMALS, starting_value=STARTING_VALUE):
    account = get_account()
    if contract_type == MockV3Aggregator:
        if len(contract_type) == 0:
            MockV3Aggregator.deploy(decimals, starting_value * (10**8), {'from': account})
            print('MockV3Aggregator deployed')

    elif contract_type == MockWETH:
        if len(contract_type) == 0:
            MockWETH.deploy({'from':account}, publish_source=config['networks'][network.show_active()]['verify'])
            print('MockWETH deployed')

    elif contract_type == MockDAI:
        if len(contract_type) == 0:
            MockDAI.deploy({'from':account}, publish_source=config['networks'][network.show_active()]['verify'])
            print('MockDAI deployed')
