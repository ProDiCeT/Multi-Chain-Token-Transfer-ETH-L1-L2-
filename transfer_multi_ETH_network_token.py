import streamlit as st
from web3 import Web3

st.set_page_config(page_title="Multi-chain Token Transfer", layout="centered")
st.title("💸 Multi-chain Token Transfer (ETH / L2 / ERC-20)")

# --- Network selection ---
network_type = st.radio("🌐 Network type", ["Mainnet", "Testnet"])

chains = {
    "Ethereum": {
        "Mainnet": {"rpc": "https://mainnet.infura.io/v3/YOUR_INFURA_KEY", "chainId": 1, "explorer": "https://etherscan.io"},
        "Testnet": {"rpc": "https://sepolia.infura.io/v3/YOUR_INFURA_KEY", "chainId": 11155111, "explorer": "https://sepolia.etherscan.io"}
    },
    "Base": {
        "Mainnet": {"rpc": "https://mainnet.base.org", "chainId": 8453, "explorer": "https://basescan.org"},
        "Testnet": {"rpc": "https://sepolia.base.org", "chainId": 84532, "explorer": "https://sepolia.basescan.org"}
    },
    "Linea": {
        "Mainnet": {"rpc": "https://rpc.linea.build", "chainId": 59144, "explorer": "https://lineascan.build"},
        "Testnet": {"rpc": "https://rpc.sepolia.linea.build", "chainId": 59141, "explorer": "https://sepolia.lineascan.build"}
    },
    "Arbitrum": {
        "Mainnet": {"rpc": "https://arb1.arbitrum.io/rpc", "chainId": 42161, "explorer": "https://arbiscan.io"},
        "Testnet": {"rpc": "https://sepolia-rollup.arbitrum.io/rpc", "chainId": 421614, "explorer": "https://sepolia.arbiscan.io"}
    },
    "Optimism": {
        "Mainnet": {"rpc": "https://mainnet.optimism.io", "chainId": 10, "explorer": "https://optimistic.etherscan.io"},
        "Testnet": {"rpc": "https://sepolia.optimism.io", "chainId": 11155420, "explorer": "https://sepolia-optimism.etherscan.io"}
    },
}

chain_name = st.selectbox("⛓️ Choose network", list(chains.keys()))
selected = chains[chain_name][network_type]
rpc_url = selected["rpc"]
chain_id = selected["chainId"]
explorer = selected["explorer"]

st.info(f"🔗 Using {chain_name} {network_type}\nRPC: `{rpc_url}`")

# --- Tokens ---
tokens = {
    "ETH": {"address": None, "decimals": 18},
    "USDC": {
        "Ethereum": {"Mainnet": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "Testnet": None},
        "Base": {"Mainnet": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", "Testnet": None},
        "Linea": {"Mainnet": "0x176211869cA2b568f2A7D4EE941E073a821EE1ff", "Testnet": None},
        "Arbitrum": {"Mainnet": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831", "Testnet": None},
        "Optimism": {"Mainnet": "0x7F5c764cBc14f9669B88837ca1490cCa17c31607", "Testnet": None},
        "decimals": 6
    },
    "WETH": {
        "Ethereum": {"Mainnet": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", "Testnet": None},
        "Base": {"Mainnet": "0x4200000000000000000000000000000000000006", "Testnet": None},
        "Linea": {"Mainnet": "0xE5caef4af8780e59df925470b050fb23c43ca68c", "Testnet": None},
        "Arbitrum": {"Mainnet": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1", "Testnet": None},
        "Optimism": {"Mainnet": "0x4200000000000000000000000000000000000006", "Testnet": None},
        "decimals": 18
    }
}

# --- Token selection ---
token_mode = st.radio("💠 Token mode", ["Standard token", "Custom ERC-20"])

if token_mode == "Standard token":
    token_name = st.selectbox("Select token", list(tokens.keys()))
else:
    st.markdown("### ➕ Add custom token")
    token_name = st.text_input("Token name (ex: MYTOKEN)").upper() or "CUSTOM"
    custom_address = st.text_input("Contract address (0x...)", "")
    custom_decimals = st.number_input("Decimals", min_value=0, max_value=18, value=18, step=1)
    if custom_address and Web3.is_address(custom_address):
        tokens[token_name] = {
            chain_name: {network_type: custom_address},
            "decimals": custom_decimals
        }
    else:
        st.warning("Enter a valid ERC-20 address to register custom token.")

# --- User inputs ---
private_key = st.text_input("🔑 Private key", type="password")
destination = st.text_input("🎯 Receiving address (0x...)")
amount = st.number_input("💰 Amount", min_value=0.0001, value=0.01, step=0.001)

col1, col2 = st.columns(2)
check_balance = col1.button("💰 Check Balance")
send_button = col2.button("🚀 Send")

# --- Options ---
def erc20_balance(w3, token_address, account):
    abi = [{"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"}]
    contract = w3.eth.contract(address=token_address, abi=abi)
    return contract.functions.balanceOf(account).call()

def send_erc20(w3, token_address, decimals, account, destination, amount, private_key):
    abi = [{"constant": False, "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "type": "function"}]
    contract = w3.eth.contract(address=token_address, abi=abi)
    value = int(amount * (10 ** decimals))
    tx = contract.functions.transfer(destination, value).build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "gas": 100000,
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return tx_hash.hex()

# --- Web3 connection ---
if check_balance or send_button:
    if not private_key.startswith("0x") or len(private_key) != 66:
        st.error("❌ Invalid private key.")
    else:
        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url))
            if not w3.is_connected():
                st.error(f"❌ Unable to connect to {chain_name} {network_type}")
            else:
                account = w3.eth.account.from_key(private_key)
                sender = account.address
                st.write(f"📤 Sender: `{sender}`")

                # Input amount verification
                if check_balance:
                    if token_name == "ETH":
                        balance = w3.eth.get_balance(sender)
                        balance_eth = w3.from_wei(balance, 'ether')
                        st.info(f"💰 ETH balance: `{balance_eth:.6f} ETH`")
                    else:
                        token_data = tokens[token_name]
                        token_address = token_data.get(chain_name, {}).get(network_type)
                        if not token_address:
                            st.warning(f"⚠️ {token_name} not available on {chain_name} {network_type}.")
                        else:
                            decimals = token_data["decimals"]
                            raw_balance = erc20_balance(w3, token_address, sender)
                            balance_token = raw_balance / (10 ** decimals)
                            st.info(f"💰 {token_name} balance: `{balance_token:.6f} {token_name}`")

                # Token sending
                if send_button:
                    if not Web3.is_address(destination):
                        st.error("❌ Invalid receiving address.")
                    elif token_name == "ETH":
                        balance = w3.eth.get_balance(sender)
                        value = w3.to_wei(amount, 'ether')
                        gas = 21000
                        gas_price = w3.eth.gas_price
                        fee = gas * gas_price
                        if balance < (value + fee):
                            st.error("❌ Insufficient funds.")
                        else:
                            tx = {"nonce": w3.eth.get_transaction_count(sender), "to": destination, "value": value, "gas": gas, "gasPrice": gas_price, "chainId": chain_id}
                            signed_tx = w3.eth.account.sign_transaction(tx, private_key)
                            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                            st.success("✅ ETH Transaction sent!")
                            st.markdown(f"🔗 [View on explorer]({explorer}/tx/{tx_hash.hex()})")
                    else:
                        token_data = tokens[token_name]
                        token_address = token_data.get(chain_name, {}).get(network_type)
                        if not token_address:
                            st.warning(f"⚠️ {token_name} not available on {chain_name} {network_type}.")
                        else:
                            decimals = token_data["decimals"]
                            tx_hash = send_erc20(w3, token_address, decimals, account, destination, amount, private_key)
                            st.success(f"✅ {token_name} transaction sent!")
                            st.markdown(f"🔗 [View on explorer]({explorer}/tx/{tx_hash})")
        except Exception as e:
            st.error(f"⚠️ Error: {e}")
