from cosmpy.aerial.wallet import LocalWallet

def get_wallet(mnemonic: str, prefix: str) -> LocalWallet:
    return LocalWallet.from_mnemonic(mnemonic, prefix)
