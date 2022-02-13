from os import access
from scripts.general_scripts import get_account
from brownie import config, network, DappToken, TokenFarm


KEPT_BALANCE = 1_000 * (10**18)


def main():
    deploy_token_farm_and_dapp_token()

def deploy_token_farm_and_dapp_token():
    account = get_account()
    dapp_token = DappToken.deploy({'from':account}, publish_source=config['networks'][network.show_active()]['verify'])
    token_farm = TokenFarm.deploy(dapp_token.address, {'from':account}, publish_source=config['networks'][network.show_active()]['verify'])

    tx = dapp_token.transfer(token_farm.address, dapp_token.totalSupply() - KEPT_BALANCE, {'from':account})
    tx.wait(1)
