<div align="center">

# 🧹 Solana Collector

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Solana](https://img.shields.io/badge/Solana-Mainnet-purple.svg?style=for-the-badge&logo=solana&logoColor=white)](https://solana.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg?style=for-the-badge)](https://github.com/fridayqq/solana_collector)

**🚀 A powerful Python toolkit for collecting and consolidating SOL tokens across multiple wallet addresses**

[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red.svg?style=flat-square)](https://github.com/fridayqq)
[![SOL](https://img.shields.io/badge/Token-SOL-blue.svg?style=flat-square)](https://coinmarketcap.com/currencies/solana/)
[![Blockchain](https://img.shields.io/badge/Blockchain-Solana-purple.svg?style=flat-square)](https://explorer.solana.com/)

---

</div>

## ✨ Features

- **💰 Balance Checker** (`checker.py`): Monitor SOL balances across Phantom and Magic Eden wallets with USD values
- **📤 Bulk Collector** (`sender.py`): Automatically collect and transfer SOL from multiple wallets to recipients
- **💵 Real-time USD Conversion**: Fetches current SOL prices from CoinGecko for accurate value calculation
- **📊 Transaction Monitoring**: Comprehensive tracking with Solscan integration and success rates
- **🔧 Multi-Wallet Support**: Supports both Phantom and Magic Eden derivation paths
- **⚡ Smart Fee Management**: Automatically reserves SOL for rent exemption and transaction fees

## 📋 Prerequisites

- ![Python](https://img.shields.io/badge/Python-3.7+-blue?logo=python&logoColor=white) Python 3.7+
- ![Internet](https://img.shields.io/badge/Internet-Connection-green) Active internet connection
- ![Wallet](https://img.shields.io/badge/Wallet-Seed_Phrases-orange) Valid Solana seed phrases

## 🚀 Installation

1. Clone or download this repository
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### For Balance Checking

Create a `seed.txt` file with your seed phrases (one per line):
```
your first twelve word seed phrase here for wallet one
your second twelve word seed phrase here for wallet two
```

### For SOL Collection

Create a `to_send.txt` file with sender seed phrases and recipient addresses:
```
sender_seed_phrase_1;recipient_solana_address_1
sender_seed_phrase_2;recipient_solana_address_2
```

## 📖 Usage

### 📊 Check Balances

Run the balance checker to see SOL balances across all wallet types:

```bash
python checker.py
```

**Output includes:**
- 👻 Phantom wallet addresses and balances
- 🎨 Magic Eden accounts (0-4) with individual balances
- 💰 SOL amounts in both tokens and USD value
- 📈 Total portfolio summary

### 💸 Collect SOL

Run the sender to automatically gather SOL from multiple wallets:

```bash
python sender.py
```

**Features:**
- 🧮 Automatically calculates sendable amount (balance - commission for fees)
- 🔧 Handles rent exemption requirements
- 🔗 Provides transaction hashes and Solscan explorer links
- ⏱️ Real-time transaction confirmation monitoring
- 📊 Comprehensive statistics tracking

## 🔐 Security Considerations

> ⚠️ **Important Security Notes:**
> - 🚫 Never share your seed phrases with anyone
> - 🔒 Keep `seed.txt` and `to_send.txt` files secure and private
> - 🧪 Test with small amounts on devnet before mainnet operations
> - ✅ Always verify recipient addresses before running sender
> - 🛡️ Files containing seed phrases are automatically ignored by Git

## 📁 File Structure

```
solana_collector/
├── 📖 README.md              # This documentation
├── 📦 requirements.txt       # Python dependencies
├── 📊 checker.py            # Balance checking utility
├── 📤 sender.py             # SOL sender script
├── 🔑 seed.txt              # Your seed phrases (ignored by Git)
├── 📋 to_send.txt           # Transfer instructions (ignored by Git)
└── 🛡️ .gitignore            # Protects sensitive files
```

## 🌐 Network Configuration

| Parameter | Value |
|-----------|-------|
| 🌍 **RPC Endpoint** | `https://api.mainnet-beta.solana.com` |
| 📈 **Price API** | `https://api.coingecko.com/api/v3/simple/price` |
| 🔍 **Explorer** | `https://solscan.io` |
| ⏱️ **Rate Limiting** | 0.5s between requests |


## 🛠️ Configuration Options

```python
NUM_ACCOUNTS = 5        # Number of Magic Eden accounts to check
MIN_BALANCE = 0.001     # Minimum balance to attempt transfer (SOL)
COMMISSION = 0.001      # Amount to leave for rent exemption (SOL)
WALLET_PAUSE = 3        # Pause between wallets (seconds)
```

## 🛠️ Error Handling

The tools include comprehensive error handling for:
- ❌ Invalid seed phrases or malformed addresses
- 🌐 Network connectivity issues and RPC timeouts
- 💸 Insufficient balances for transfers
- 🔄 Transaction failures and confirmation errors
- ⏱️ API rate limits and retry mechanisms

## ⛽ Transaction Economics

| Parameter | Typical Value |
|-----------|---------------|
| 🏃‍♂️ **Transaction Fee** | ~0.000005 SOL |
| 💰 **Rent Exemption** | ~0.00203928 SOL |
| 📊 **Reserved Amount** | 0.001 SOL (configurable) |
| 🛡️ **Safety Buffer** | Prevents account closure |

## 📄 Example Output

### 📊 Balance Checker
```
Текущий курс SOL: $85.42

=== Сидка #1: example seed phrase words here ===
Phantom Address: 9WzDXw...tAWWM | Balance: 0.156789 SOL ($13.40)
Account 0 | Address: 3HNXQt...yssh | Balance: 0.029023 SOL ($2.48)
Account 1 | Address: 5Ky8Vb...mNp7 | Balance: 0.000000 SOL ($0.00)
Сумма по сидке: 0.185812 SOL ($15.88)

==================================================
ОБЩАЯ СУММА: 0.185812 SOL ($15.88)
```

### 🧹 SOL sender
```
🚀 Начинаем обработку 2 кошельков...

📝 Кошелек 1/2
Recipient: 9WzD...WWM

Phantom  | Address: 3HNXQTX...vBaRdMBryssh | Balance: 0.029023 SOL
   Отправляем 0.028023 SOL (Phantom)...
   ✅ Транзакция успешна: 2Cnbe4B2mKYav...dJm2
   Solscan: https://solscan.io/tx/2Cnbe4B2mKYav...dJm2

============================================================
📊 ИТОГОВАЯ СТАТИСТИКА
============================================================
Обработано кошельков: 2
✅ Успешных переводов: 3
❌ Неудачных переводов: 0
💰 Всего отправлено SOL: 0.456789
📈 Процент успеха: 100.0%
============================================================
```

## 🔗 Useful Resources

- 📚 [Solana Documentation](https://docs.solana.com/)
- 🔍 [Solscan Explorer](https://solscan.io/)
- 👻 [Phantom Wallet](https://phantom.app/)
- 🎨 [Magic Eden](https://magiceden.io/)
- 💰 [CoinGecko API](https://www.coingecko.com/en/api)

---

<div align="center">

## 📜 Disclaimer

**This software is provided "as is" without warranty. Users are responsible for:**

🔐 Securing their seed phrases • ✅ Verifying transaction details • ⛽ Understanding Solana network fees • 📋 Complying with applicable regulations

**⚠️ Use at your own risk. Always test with small amounts first.**

---

Made with ❤️ for the Solana community

[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=social&logo=github)](https://github.com/fridayqq)
[![Solana](https://img.shields.io/badge/Solana-Explorer-purple?style=social&logo=solana)](https://explorer.solana.com/)

</div>
