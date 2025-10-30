# 💸 Multi-Chain Token Transfer (ETH / ERC-20 / L2)

A simple **Streamlit + Web3.py** interface to send tokens across **Ethereum L1** and **L2 networks**  
(Base, Linea, Arbitrum, Optimism), with support for both **Mainnet** and **Testnet** (Sepolia).

---

## 🚀 Features

✅ Select between **Mainnet** or **Testnet**  
✅ Supports **ETH native transfers** and **ERC-20 tokens** (USDC, WETH, etc.)  
✅ Add **custom ERC-20 tokens** manually (address + decimals)  
✅ **Check your balance** before sending (ETH or ERC-20)  
✅ Automatic **block explorer link** after each transaction  
✅ **Private key** is hidden for safety  

---

## ⚙️ Installation

```bash
git clone https://github.com/<your_repo>/multi-chain-transfer.git
cd multi-chain-transfer
pip install streamlit web3

▶️ Usage

streamlit run transfer_multi_network_token.py

Then open the local link displayed in your terminal (usually http://localhost:8501

).
🔧 Supported Networks
Layer	Network	RPC Example	Explorer
L1	Ethereum Mainnet	https://mainnet.infura.io/v3/YOUR_INFURA_KEY	etherscan.io
L1	Ethereum Testnet	https://sepolia.infura.io/v3/YOUR_INFURA_KEY	sepolia.etherscan.io
L2	Base	https://mainnet.base.org	basescan.org
L2	Linea	https://rpc.linea.build	lineascan.build
L2	Arbitrum	https://arb1.arbitrum.io/rpc	arbiscan.io
L2	Optimism	https://mainnet.optimism.io	optimistic.etherscan.io

    🧠 Replace YOUR_INFURA_KEY with your own Infura project key, or use a public RPC endpoint.

🧩 How to Use

    Select network layer and token type

    Enter your private key (hidden input)

    Click 💰 Check Balance to verify available funds

    Enter destination address and amount

    Click 🚀 Send to broadcast the transaction

    A link to the transaction explorer will appear on success

➕ Add Custom ERC-20 Tokens

You can easily send any custom ERC-20 token by:

    Choosing “Custom ERC-20” mode

    Entering:

        Token name

        Contract address

        Decimals

    The app will register your token and use it for balance check & transfer.

🔒 Security Notes

    Never share your private key — this app is for local or educational use only

    Always test on Sepolia or other testnets before using real funds

    For production environments, integrate MetaMask or WalletConnect instead of direct key entry

🧠 Coming Soon

    Dynamic gas estimation (Low / Normal / Fast)

    Automatic ERC-20 balance verification before sending

    Transaction history log

👨‍💻 Author: made with love by dnapog
🔗 Built with Streamlit + Web3.py
