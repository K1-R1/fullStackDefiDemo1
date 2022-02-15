from brownie import TokenFarm
from scripts.general_scripts import get_account


def issue_token():
    account = get_account()
    token_farm = TokenFarm[-1]
    token_farm.issueTokens({"from": account}).wait(1)


def main():
    issue_token()