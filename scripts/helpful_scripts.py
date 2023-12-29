from brownie import network, accounts, config

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "sepolia",
    "development",
    "ganache",
    "hardhat",
    "local-ganache",
    "mainnet-fork",
]

# network.connect("sepolia")


def get_account(index=None, id=None):
    # if index:
    #     return accounts[index]
    # if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
    #     print(accounts[0].balance())
    #     return accounts[0]
    # if id:
    #     return accounts.load(id)
    if network.show_active() in config["networks"]:
        return accounts.add(config["wallets"]["from_key"])