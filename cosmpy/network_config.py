from cosmpy.aerial.client import NetworkConfig

from cosmos_directory.common import get_fee_denom


def set_network_config(network: dict):
    try:
        fee_denom = get_fee_denom(network)
        gas_price = network.fees.fee_tokens[0].fixed_min_gas_price
    except Exception:
        gas_price = 1

    return NetworkConfig(
        chain_id=network.chain_id,
        url=f"rest+https://{network.chain_name}-api.lavenderfive.com:443",
        fee_minimum_gas_price=gas_price,
        fee_denomination=fee_denom,
        staking_denomination=fee_denom,
    )
