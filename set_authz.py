import os

from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin
from cosmpy.aerial.client.utils import prepare_and_broadcast_basic_transaction
from cosmpy.aerial.tx import Transaction

from datetime import datetime, timedelta

from google.protobuf import any_pb2, timestamp_pb2
from cosmpy.protos.cosmos.authz.v1beta1.authz_pb2 import Grant
from cosmpy.protos.cosmos.authz.v1beta1.tx_pb2 import MsgGrant
from cosmpy.protos.cosmos.bank.v1beta1.authz_pb2 import SendAuthorization

from dotenv import load_dotenv

from cosmpy_utils.common import get_ledger, get_wallet
from cosmos_directory.common import get_chain_registry_info, get_denom
from cosmpy_utils.network_config import set_network_config

load_dotenv()

GRANTER_MNEMONIC = os.getenv('GRANTER_MNEMONIC')

def get_denom_type(denom: str) -> int:
    prefix = denom[0]
    if prefix == 'u':
        return 6
    elif prefix == 'n':
        return 9
    elif prefix == 'a':
        return 18

def main(network_name: str):
    chain_registry = get_chain_registry_info(network_name)
    prefix = chain_registry.get("bech32_prefix")
    granter_wallet = get_wallet(GRANTER_MNEMONIC, prefix)
    denom = get_denom(chain_registry)
    denom_type = get_denom_type(denom)
    amount = 1000*(10**denom_type)

    ledger = get_ledger(chain_registry)

    # Set total authorization time and spend amount
    total_authz_time = 100000000
    spend_amount = Coin(amount=str(amount), denom=denom)

    # Authorize authz_wallet to send tokens from wallet
    authz_any = any_pb2.Any()
    authz_any.Pack(
        SendAuthorization(spend_limit=[spend_amount]),
        "",
    )

    expiry = timestamp_pb2.Timestamp()
    expiry.FromDatetime(datetime.now() + timedelta(seconds=total_authz_time * 60))
    grant = Grant(authorization=authz_any, expiration=expiry)

    grantee_mnemonic = os.getenv('GRANTEE_S1')
    grantee_wallet = get_wallet(grantee_mnemonic, prefix)

    msg = MsgGrant(
        granter=str(granter_wallet.address()),
        grantee=str(grantee_wallet.address()),
        grant=grant,
    )

    tx = Transaction()
    tx.add_message(msg)

    tx = prepare_and_broadcast_basic_transaction(ledger, tx, granter_wallet)
    tx.wait_to_complete()

if __name__ == "__main__":
    main(network_name="osmosis")
