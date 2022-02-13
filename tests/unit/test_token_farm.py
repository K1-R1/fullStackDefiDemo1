from scripts.general_scripts import get_account, get_contract
from scripts.deploy import deploy_token_farm_and_dapp_token
from brownie import config, network
import pytest


INITIAL_PRICE_FEED_VALUE = 2_000 * (10**18)
KEPT_BALANCE = 1_000 * (10**18)


def test_set_price_feed_contract():
    # Arrange
    if not config['networks'][network.show_active()]['local'] is True:
        pytest.skip('Only tested on local networks')
    account = get_account()
    non_owner = get_account(index=1)
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    # Act
    token_farm.setPriceFeedContract(dapp_token.address, get_contract("eth_usd_price_feed"), {"from": account}).wait(1)
    # Assert
    assert token_farm.tokenPriceFeedMapping(dapp_token.address) == get_contract("eth_usd_price_feed")
    with pytest.raises(AttributeError):
        token_farm.setPriceFeedContract(dapp_token.address, get_contract("eth_usd_price_feed"), {"from": non_owner})

def test_stake_tokens(amount_staked):
    # Arrange
    if not config['networks'][network.show_active()]['local'] is True:
        pytest.skip('Only tested on local networks')
    account = get_account()
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    # Act
    dapp_token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeTokens(amount_staked, dapp_token.address, {"from": account}).wait(1)
    # Assert
    assert (token_farm.stakingBalance(dapp_token.address, account.address) == amount_staked)
    assert token_farm.uniqueTokensStaked(account.address) == 1
    assert token_farm.stakers(0) == account.address

    return token_farm, dapp_token
    
def test_issue_tokens(amount_staked):
    # Arrange
    if not config['networks'][network.show_active()]['local'] is True:
        pytest.skip('Only tested on local networks')
    account = get_account()
    token_farm, dapp_token = test_stake_tokens(amount_staked)
    starting_balance = dapp_token.balanceOf(account.address)
    # Act
    token_farm.issueTokens({"from": account})
    # Assert
    assert (dapp_token.balanceOf(account.address) == starting_balance + INITIAL_PRICE_FEED_VALUE)

def test_add_allowed_tokens():
    # Arrange
    if not config['networks'][network.show_active()]['local'] is True:
        pytest.skip('Only tested on local networks')
    account = get_account()
    non_owner = get_account(index=1)
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    # Act
    token_farm.addAllowedTokens(dapp_token.address, {"from": account})
    # Assert
    assert token_farm.allowedTokens(0) == dapp_token.address
    with pytest.raises(AttributeError):
        token_farm.addAllowedTokens(dapp_token.address, {"from": non_owner})

def test_token_is_allowed():
    # Arrange
    if not config['networks'][network.show_active()]['local'] is True:
        pytest.skip('Only tested on local networks')
    account = get_account()
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    # Act
    test_add_allowed_tokens()
    token_is_allowed = token_farm.tokenIsAllowed(dapp_token.address, {"from": account})
    # Assert
    assert token_is_allowed is True

def test_stake_unapproved_tokens(random_erc20, amount_staked):
    # Arrange
    if not config['networks'][network.show_active()]['local'] is True:
        pytest.skip('Only tested on local networks')
    account = get_account()
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    # Act
    random_erc20.approve(token_farm.address, amount_staked, {"from": account})
    # Assert
    with pytest.raises(AttributeError):
        token_farm.stakeTokens(amount_staked, random_erc20.address, {"from": account})

def test_unstake_tokens(amount_staked):
    # Arrange
    if not config['networks'][network.show_active()]['local'] is True:
        pytest.skip('Only tested on local networks')
    account = get_account()
    token_farm, dapp_token = test_stake_tokens(amount_staked)
    # Act
    token_farm.unstakeTokens(dapp_token.address, {"from": account})
    # Assert
    assert dapp_token.balanceOf(account.address) == KEPT_BALANCE
    assert token_farm.stakingBalance(dapp_token.address, account.address) == 0
    assert token_farm.uniqueTokensStaked(account.address) == 0