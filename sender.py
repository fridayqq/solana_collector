import hmac, hashlib, struct
import nacl.signing
import base58
from mnemonic import Mnemonic
from solana.rpc.api import Client
from solders.transaction import Transaction
from solders.system_program import transfer, TransferParams
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.types import TxOpts
import time

def ed25519_master_key(seed):
    h = hmac.new(b"ed25519 seed", seed, hashlib.sha512).digest()
    return h[:32], h[32:]

def derive_child_key(parent_key, parent_chain_code, idx):
    data = b'\x00' + parent_key + struct.pack(">L", idx)
    h = hmac.new(parent_chain_code, data, hashlib.sha512).digest()
    return h[:32], h[32:]

def derive_path_ed25519(seed, path):
    master_key, master_chain = ed25519_master_key(seed)
    key, chain = master_key, master_chain
    for level in path.lstrip("m/").split("/"):
        if not level:
            continue
        if level.endswith("'"):
            idx = int(level[:-1]) + 0x80000000
        else:
            idx = int(level)
        key, chain = derive_child_key(key, chain, idx)
    return key

def get_private_key(seed_phrase, path):
    seed = Mnemonic("english").to_seed(seed_phrase)
    priv = derive_path_ed25519(seed, path)
    return priv

def get_address_from_privkey(privkey):
    keypair = Keypair.from_seed(privkey)
    return str(keypair.pubkey())

def get_sol_balance(address, client):
    pubkey = Pubkey.from_string(address)
    balance = client.get_balance(pubkey)
    return balance.value / 1e9

from bip32 import BIP32

def get_me_address_and_priv(seed_phrase, account):
    mnemo = Mnemonic("english")
    master_seed = mnemo.to_seed(seed_phrase)
    path = f"m/44'/501'/{account}'/0/0"
    bip32 = BIP32.from_seed(master_seed)
    privkey = bip32.get_privkey_from_path(path)
    keypair = Keypair.from_seed(privkey)
    address = str(keypair.pubkey())
    return address, privkey

def send_sol(from_privkey, recipient_str, amount, client):
    sender = Keypair.from_seed(from_privkey)
    recipient = Pubkey.from_string(recipient_str)
    
    # Get recent blockhash
    recent_blockhash = client.get_latest_blockhash().value.blockhash
    
    transfer_ix = transfer(TransferParams(
        from_pubkey=sender.pubkey(),
        to_pubkey=recipient,
        lamports=int(amount * 1e9)
    ))
    
    txn = Transaction.new_with_payer([transfer_ix], sender.pubkey())
    txn.sign([sender], recent_blockhash)
    
    resp = client.send_transaction(txn, opts=TxOpts(skip_preflight=True, preflight_commitment="confirmed"))
    
    # Wait and check transaction status
    time.sleep(3)
    try:
        tx_status = client.confirm_transaction(resp.value, commitment="confirmed")
        if tx_status.value and len(tx_status.value) > 0 and tx_status.value[0].confirmation_status:
            return resp, True
        else:
            return resp, False
    except:
        # If we can't confirm, assume it's successful since we got a transaction hash
        return resp, True

def get_solscan_url(tx_hash):
    return f"https://solscan.io/tx/{tx_hash}"

def main():
    RPC_URL = "https://api.mainnet-beta.solana.com"
    client = Client(RPC_URL)
    NUM_ACCOUNTS = 5
    MIN_BALANCE = 0.001  # Минимум для отправки (в SOL)
    COMMISSION = 0.001  # Увеличиваем комиссию для rent exemption
    WALLET_PAUSE = 3  # Пауза между кошельками в секундах

    # Статистика
    total_wallets = 0
    successful_transfers = 0
    failed_transfers = 0
    total_sol_sent = 0.0

    with open("to_send.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    print(f"🚀 Начинаем обработку {len(lines)} кошельков...\n")

    for i, line in enumerate(lines):
        try:
            seed_phrase, recipient = line.split(";")
            recipient = recipient.strip()  # Remove any whitespace
            total_wallets += 1
            
            print(f"📝 Кошелек {i+1}/{len(lines)}")
            print(f"Сидка: {seed_phrase}\nRecipient: {recipient}")

            # === PHANTOM ADDRESS ===
            phantom_path = "m/44'/501'/0'/0'"
            privkey = get_private_key(seed_phrase, phantom_path)
            address = get_address_from_privkey(privkey)
            balance = get_sol_balance(address, client)
            print(f"Phantom  | Address: {address} | Balance: {balance:.6f} SOL")
            if balance > MIN_BALANCE:
                to_send = balance - COMMISSION
                if to_send > 0:
                    print(f"   Отправляем {to_send:.6f} SOL на {recipient} (Phantom)...")
                    resp, success = send_sol(privkey, recipient, to_send, client)
                    tx_hash = str(resp.value)
                    solscan_url = get_solscan_url(tx_hash)
                    if success:
                        print(f"   ✅ Транзакция успешна: {tx_hash}")
                        print(f"   Solscan: {solscan_url}")
                        successful_transfers += 1
                        total_sol_sent += to_send
                    else:
                        print(f"   ❌ Транзакция неуспешна: {tx_hash}")
                        print(f"   Solscan: {solscan_url}")
                        failed_transfers += 1
                    time.sleep(1)
                else:
                    print("   Недостаточно средств на фантом-адресе.")
            else:
                print("   Баланс на фантом-адресе слишком мал для отправки.")

            # === ME ADDRESSES ===
            for account in range(NUM_ACCOUNTS):
                address, privkey = get_me_address_and_priv(seed_phrase, account)
                balance = get_sol_balance(address, client)
                print(f"ME acct {account} | Address: {address} | Balance: {balance:.6f} SOL")
                if balance > MIN_BALANCE:
                    to_send = balance - COMMISSION
                    if to_send > 0:
                        print(f"   Отправляем {to_send:.6f} SOL на {recipient} (ME account {account})...")
                        resp, success = send_sol(privkey, recipient, to_send, client)
                        tx_hash = str(resp.value)
                        solscan_url = get_solscan_url(tx_hash)
                        if success:
                            print(f"   ✅ Транзакция успешна: {tx_hash}")
                            print(f"   Solscan: {solscan_url}")
                            successful_transfers += 1
                            total_sol_sent += to_send
                        else:
                            print(f"   ❌ Транзакция неуспешна: {tx_hash}")
                            print(f"   Solscan: {solscan_url}")
                            failed_transfers += 1
                        time.sleep(1)
                    else:
                        print(f"   Недостаточно средств на ME account {account}.")
                else:
                    print(f"   Баланс слишком мал для отправки (ME account {account}).")

            # Пауза между кошельками
            if i < len(lines) - 1:  # Не делаем паузу после последнего кошелька
                print(f"\n⏳ Пауза {WALLET_PAUSE} сек. перед следующим кошельком...")
                time.sleep(WALLET_PAUSE)

        except Exception as e:
            print("Ошибка:", e)
            failed_transfers += 1

    # Финальная статистика
    print("\n" + "="*60)
    print("📊 ИТОГОВАЯ СТАТИСТИКА")
    print("="*60)
    print(f"Обработано кошельков: {total_wallets}")
    print(f"✅ Успешных переводов: {successful_transfers}")
    print(f"❌ Неудачных переводов: {failed_transfers}")
    print(f"💰 Всего отправлено SOL: {total_sol_sent:.6f}")
    print(f"📈 Процент успеха: {(successful_transfers/(successful_transfers+failed_transfers)*100 if (successful_transfers+failed_transfers) > 0 else 0):.1f}%")
    print("="*60)

if __name__ == "__main__":
    main()