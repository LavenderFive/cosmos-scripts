from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin
from cosmpy.aerial.client.utils import prepare_and_broadcast_basic_transaction
from cosmpy.aerial.tx import Transaction

from datetime import datetime, timedelta

from google.protobuf import any_pb2, timestamp_pb2
from cosmpy.protos.cosmos.authz.v1beta1.authz_pb2 import Grant
from cosmpy.protos.cosmos.authz.v1beta1.tx_pb2 import MsgGrant
from cosmpy.protos.cosmos.bank.v1beta1.authz_pb2 import SendAuthorization


def main():
    # Set total authorization time and spend amount
    total_authz_time = 100000000
    amount = 1000000000000000000
    spend_amount = Coin(amount=str(amount), denom="atestfet")

    # Authorize authz_wallet to send tokens from wallet
    authz_any = any_pb2.Any()
    authz_any.Pack(
        SendAuthorization(spend_limit=[spend_amount]),
        "",
    )

    expiry = timestamp_pb2.Timestamp()
    expiry.FromDatetime(datetime.now() + timedelta(seconds=total_authz_time * 60))
    grant = Grant(authorization=authz_any, expiration=expiry)

    msg = MsgGrant(
        granter=str(wallet.address()),
        grantee=str(authz_wallet.address()),
        grant=grant,
    )

    tx = Transaction()
    tx.add_message(msg)

    tx = prepare_and_broadcast_basic_transaction(ledger, tx, wallet)
    tx.wait_to_complete()

if __name__ == "__main__":
    main()
