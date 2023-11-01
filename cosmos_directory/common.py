from common.common import request_json


def get_chain_registry_info(network_name: str) -> dict:
    network_url = get_chain_url(network_name)
    return request_json(network_url)["chain"]


def get_chain_url(network_name: str) -> str:
    return f"https://chains.cosmos.directory/{network_name}"


def get_rest_cosmos_directory(network_name: str) -> str:
    return f"https://rest.cosmos.directory:443/{network_name}"


def get_rpc_cosmos_directory(network_name: str) -> str:
    return f"https://rpc.cosmos.directory:443/{network_name}"


def get_denom(registry_info: dict) -> str:
    return registry_info["staking"]["staking_tokens"][0]["denom"]


def get_fee_denom(network: dict) -> str:
    if "fees" in network:
        return network["fees"]["fee_tokens"][0]["denom"]
    elif "staking" in network:
        return network["staking"]["staking_tokens"][0]["denom"]
    else:
        error_message = f"Error getting staking tokens for {network['chain_name']}"
        raise Exception(error_message)
