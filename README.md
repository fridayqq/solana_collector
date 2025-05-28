# 🧹 Solana Garbage Collector

A powerful Python tool for collecting and consolidating SOL tokens from multiple wallet addresses derived from seed phrases. Perfect for cleaning up scattered funds across Phantom wallet and Magic Eden accounts.

## 🎯 Project Overview

```mermaid
graph TD
    A[📝 Seed Phrases] --> B[🔍 Address Discovery]
    B --> C[👻 Phantom Wallet]
    B --> D[🎨 Magic Eden Accounts 0-4]
    C --> E[💰 Balance Check]
    D --> E
    E --> F{Balance > MIN?}
    F -->|Yes| G[💸 Transfer SOL]
    F -->|No| H[⏭️ Skip Address]
    G --> I[✅ Transaction Success]
    G --> J[❌ Transaction Failed]
    I --> K[📊 Update Stats]
    J --> K
    K --> L[🔗 Solscan Link]
```

## 🏗️ Architecture Flow

```mermaid
sequenceDiagram
    participant U as User
    participant C as Collector
    participant S as Solana RPC
    participant R as Recipient
    
    U->>C: Load seed phrases
    U->>C: Start collection
    
    loop For each seed phrase
        C->>S: Derive addresses
        C->>S: Check balances
        alt Balance > MIN_BALANCE
            C->>S: Create transaction
            C->>S: Send SOL
            S->>R: Transfer complete
            C->>U: Show success ✅
        else
            C->>U: Skip (low balance) ⏭️
        end
    end
    
    C->>U: Final statistics 📊
```

## ✨ Features

- 🔍 **Multi-wallet scanning**: Checks both Phantom and Magic Eden wallet addresses
- 💸 **Automated transfers**: Sends all available SOL to specified recipient addresses
- 📊 **Real-time statistics**: Tracks successful/failed transactions and total SOL sent
- 🔗 **Solscan integration**: Provides direct links to transaction details
- ⏱️ **Rate limiting**: Configurable delays to avoid RPC throttling
- 💰 **Price tracking**: Shows USD values using live SOL prices
- 🛡️ **Error handling**: Robust error handling with retry mechanisms

## 📁 Project Structure

```
solana_garbage_collector/
├── 📄 README.md                 # This file
├── 📋 requirements.txt          # Python dependencies
├── 📤 sender.py               # Sender script
├── 🔍 checker.py              # Balance checking utility
├── 🌱 seed.txt                # Your seed phrases (one per line)
└── 📮 to_send.txt             # Seed phrase and recipient pairs
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
git clone <your-repo-url>
cd solana_garbage_collector

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create your input files:

**seed.txt** - List your seed phrases (one per line):
```
your first seed phrase here
your second seed phrase here
```

**to_send.txt** - Map seed phrases to recipient addresses:
```
your first seed phrase here;9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM
your second seed phrase here;9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM
```

### 3. Usage Workflow

```mermaid
graph LR
    A[📁 Setup Files] --> B[🔍 Check Balances]
    B --> C{Found SOL?}
    C -->|Yes| D[🚀 Run Collector]
    C -->|No| E[😴 Nothing to do]
    D --> F[📊 View Results]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style D fill:#e8f5e8
    style F fill:#fff3e0
```

#### Check Balances First
```bash
python checker.py
```
This will show you all balances across Phantom and Magic Eden wallets with USD values.

#### Collect and Send SOL
```bash
python collector.py
```
This will automatically collect SOL from all discovered addresses and send to recipients.

## 🔧 Configuration Options

Edit the constants in `collector.py`:

```python
NUM_ACCOUNTS = 5        # Number of Magic Eden accounts to check
MIN_BALANCE = 0.001     # Minimum balance to attempt transfer (SOL)
COMMISSION = 0.001      # Amount to leave for rent exemption (SOL)
WALLET_PAUSE = 3        # Pause between wallets (seconds)
```

## 📊 Address Types Supported

```mermaid
graph TB
    A[🌱 Seed Phrase] --> B[🔑 BIP44 Derivation]
    B --> C[👻 Phantom<br/>m/44'/501'/0'/0']
    B --> D[🎨 Magic Eden 0<br/>m/44'/501'/0'/0/0]
    B --> E[🎨 Magic Eden 1<br/>m/44'/501'/1'/0/0]
    B --> F[🎨 Magic Eden 2<br/>m/44'/501'/2'/0/0]
    B --> G[🎨 Magic Eden 3<br/>m/44'/501'/3'/0/0]
    B --> H[🎨 Magic Eden 4<br/>m/44'/501'/4'/0/0]
    
    style A fill:#ffeb3b
    style C fill:#9c27b0
    style D fill:#ff5722
    style E fill:#ff5722
    style F fill:#ff5722
    style G fill:#ff5722
    style H fill:#ff5722
```

## 🛡️ Security Features

- ✅ Rent exemption protection (leaves small amount for account rent)
- ✅ Transaction confirmation checking
- ✅ Proper error handling and retries
- ✅ Rate limiting to prevent RPC throttling

## 📈 Sample Output

```
🚀 Начинаем обработку 2 кошельков...

📝 Кошелек 1/2
Сидка: 
Recipient: 

Phantom  | Address:  | Balance: 0.029023 SOL
   Отправляем 0.028023 SOL на  (Phantom)...
   ✅ Транзакция успешна: 
   Solscan: https://solscan.io/tx/

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

## 💡 Process Visualization

```mermaid
pie title Transaction Results
    "Successful Transfers" : 85
    "Failed Transfers" : 10
    "Skipped (Low Balance)" : 5
```

## ⚠️ Important Notes

- **Testnet vs Mainnet**: Currently configured for Solana mainnet. Change RPC_URL for testnet.
- **Gas Fees**: Each transaction costs ~0.000005 SOL in fees.
- **Rent Exemption**: Solana accounts need ~0.00203928 SOL for rent exemption.
- **Rate Limits**: Free RPC endpoints have rate limits. Consider using paid RPC for heavy usage.

## 🔗 Useful Links

- [Solana Documentation](https://docs.solana.com/)
- [Solscan Explorer](https://solscan.io/)
- [Phantom Wallet](https://phantom.app/)
- [Magic Eden](https://magiceden.io/)

## 📝 License

This project is for educational purposes. Use responsibly and ensure you have proper authorization for all wallet addresses being accessed.

**⚠️ Disclaimer**: Always test with small amounts first. This tool handles real cryptocurrency transactions. Use at your own risk.
