from scripts.helpful_scripts import get_account
from scripts.get_weth import get_weth
from brownie import config, network, interface
from web3 import Web3


amount = Web3.toWei(0.1, "ether")

def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["sepolia"]:
        get_weth()
    # ABI
    # Addresses
    lending_pools = get_lending_pool()
    print(lending_pools)
    approve_erc20(amount, lending_pools.address, erc20_address, account)
    print("Depositing.......")
    lending_pools.deposit(erc20_address, amount, account.address, 0, {"from": account})
    tx.wait(1)
    print("Deposited....")
    borrowable_eth, total_debt = get_borrowable_data(lending_pools, account)
    print("Let's borrow")
    # DAI in terms of ETH
    dai_eth_price = get_asset_price(config["networks"][network.show_active()]["dai_eth_price_feed"])

def get_asset_price(price_feed_address):
    dai_eth_price_feed = interface.IAggregatorV3interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    print(f"The DAI/ETH price is {latest_price}")
    return float(latest_price)

def get_borrowable_data(lending_pools, account):
    (
        total_collateral_eth, 
        total_debt_eth, 
        available_borrow_eth,
        current_liquidation_threshhold, 
        ltv, 
        health_factor,
    ) = lending_pools.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(f"You have {total_collateral_eth} worth of ETH deposited")
    print(f"You have {total_debt_eth} worth of ETH borrowed")
    print(f"You have {available_borrow_eth} worth of ETH")
    return(float(available_borrow_eth), float(total_debt_eth))

def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 token")
    # ABI
    # Address
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved")
    return tx


def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(config["networks"][network.show_active()]["lending_pool_addresses_provider"])
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    # ABI
    # Address - Check
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
    

