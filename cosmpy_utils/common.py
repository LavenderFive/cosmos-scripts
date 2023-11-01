from cosmpy.aerial.wallet import LocalWallet
from cosmpy.aerial.client import LedgerClient

from cosmpy_utils.network_config import set_network_config

def get_wallet(mnemonic: str, prefix: str) -> LocalWallet:
    return LocalWallet.from_mnemonic(mnemonic, prefix)

def get_ledger(registry_info: dict) -> LedgerClient:
    cfg = set_network_config(registry_info)
    return LedgerClient(cfg)
