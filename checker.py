from mnemonic import Mnemonic
from bip32 import BIP32
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
import time
import requests
import hmac, hashlib, struct
import nacl.signing
import base58

def get_solana_address_from_seed(seed_phrase, account):
    mnemo = Mnemonic("english")
    master_seed = mnemo.to_seed(seed_phrase)
    path = f"m/44'/501'/{account}'/0/0"
    bip32 = BIP32.from_seed(master_seed)
    privkey = bip32.get_privkey_from_path(path)
    keypair = Keypair.from_seed(privkey)
    address = str(keypair.pubkey())
    return address

def ed25519_master_key(seed):
    h = hmac.new(b"ed25519 seed", seed, hashlib.sha512).digest()
    return h[:32], h[32:]

def derive_child_key(parent_key, parent_chain_code, idx):
    data = b'\x00' + parent_key + struct.pack(">L", idx)
    h = hmac.new(parent_chain_code, data, hashlib.sha512).digest()
    return h[:32], h[32:]

def derive_path_ed25519(seed, path="m/44'/501'/0'/0'"):
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

def get_phantom_address_from_seed(seed_phrase):
    seed = Mnemonic("english").to_seed(seed_phrase)
    priv = derive_path_ed25519(seed, "m/44'/501'/0'/0'")
    signing_key = nacl.signing.SigningKey(priv)
    pub = signing_key.verify_key.encode()
    address = base58.b58encode(pub).decode()
    return address

def get_sol_price():
    """Get current SOL price in USD from CoinGecko API"""
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd")
        data = response.json()
        return data['solana']['usd']
    except Exception:
        return None

def get_solana_balance(address, rpc_url="https://api.mainnet-beta.solana.com", retries=3):
    client = Client(rpc_url)
    pubkey = Pubkey.from_string(address)
    
    for attempt in range(retries):
        try:
            balance = client.get_balance(pubkey)
            return balance.value / 1e9
        except Exception as e:
            if attempt < retries - 1:
                print(f"Попытка {attempt + 1} не удалась, повторяем через 1 сек...")
                time.sleep(1)
            else:
                print(f"Все попытки исчерпаны: {e}")
                return None

def main():
    NUM_ACCOUNTS = 5   # сколько account адресов перебирать для каждой сидки
    RPC_URL = "https://api.mainnet-beta.solana.com"
    RATE_LIMIT_DELAY = 0.5  # задержка между запросами в секундах

    # Получаем текущий курс SOL
    sol_price = get_sol_price()
    if sol_price:
        print(f"Текущий курс SOL: ${sol_price:.2f}")
    else:
        print("Не удалось получить курс SOL")

    with open("seed.txt", "r", encoding="utf-8") as f:
        seeds = [line.strip() for line in f if line.strip()]

    total_sol = 0.0

    for i, seed_phrase in enumerate(seeds):
        print(f"\n=== Сидка #{i+1}: {seed_phrase} ===")
        seed_total = 0.0

        # --- Проверка баланса Phantom адреса ---
        try:
            phantom_address = get_phantom_address_from_seed(seed_phrase)
            phantom_balance = get_solana_balance(phantom_address, RPC_URL)
            if phantom_balance is not None:
                seed_total += phantom_balance
                total_sol += phantom_balance
                
                if sol_price:
                    usd_value = phantom_balance * sol_price
                    print(f"Phantom Address: {phantom_address} | Balance: {phantom_balance:.6f} SOL (${usd_value:.2f})")
                else:
                    print(f"Phantom Address: {phantom_address} | Balance: {phantom_balance:.6f} SOL")
            else:
                print(f"Phantom Address: {phantom_address} | Balance: Ошибка получения баланса")
        except Exception as e:
            print(f"Phantom Address | Ошибка: {e}")

        # Rate limiting после Phantom
        time.sleep(RATE_LIMIT_DELAY)

        # --- Проверка баланса остальных аккаунтов (Magic Eden/прочие кошельки) ---
        for account in range(NUM_ACCOUNTS):
            try:
                address = get_solana_address_from_seed(seed_phrase, account)
                balance = get_solana_balance(address, RPC_URL)
                
                if balance is not None:
                    seed_total += balance
                    total_sol += balance
                    
                    if sol_price:
                        usd_value = balance * sol_price
                        print(f"Account {account} | Address: {address} | Balance: {balance:.6f} SOL (${usd_value:.2f})")
                    else:
                        print(f"Account {account} | Address: {address} | Balance: {balance:.6f} SOL")
                else:
                    print(f"Account {account} | Address: {address} | Balance: Ошибка получения баланса")
                
                # Rate limiting
                time.sleep(RATE_LIMIT_DELAY)
                
            except Exception as e:
                print(f"Account {account} | Ошибка: {e}")
        
        # Показываем сумму по сидке
        if sol_price:
            seed_usd = seed_total * sol_price
            print(f"Сумма по сидке: {seed_total:.6f} SOL (${seed_usd:.2f})")
        else:
            print(f"Сумма по сидке: {seed_total:.6f} SOL")

    # Показываем общую сумму
    print(f"\n{'='*50}")
    if sol_price:
        total_usd = total_sol * sol_price
        print(f"ОБЩАЯ СУММА: {total_sol:.6f} SOL (${total_usd:.2f})")
    else:
        print(f"ОБЩАЯ СУММА: {total_sol:.6f} SOL")

if __name__ == "__main__":
    main()
