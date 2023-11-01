def get_fee_denom(network: dict) -> str:
    if "fees" in network:
        return network.fees.fee_tokens[0].denom
    elif "staking" in network:
        return network.staking.staking_tokens[0].denom
    else:
        error_message = f"Error getting staking tokens for {network.chain_name}"
        raise Exception(error_message)
