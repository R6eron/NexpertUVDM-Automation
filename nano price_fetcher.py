# price_fetcher.py - Lambo™ Nitro Price Oracle v2.1: FTSO Primary Smooth Blanket
# FTSO (Flare consensus XLM/USD) lead, seamless fallbacks: MEXC, Binance, CoinGecko
# 4-space indent, no trailing spaces, Termux/S20 paste-proof - ONE seamless block

import ccxt
import requests
import time
from web3 import Web3

SYMBOL = 'XLM/USDT'
COINGECKO_ID = 'stellar'
COINGECKO_VS = 'usd'
FLARE_RPC = "https://flare-api.flare.network/ext/bc/C/rpc"  # HTTPS for simplicity/mobile
FTSO_V2_ADDRESS = "0x1000000000000000000000000000000000000003"  # FtsoV2 contract
XLM_USD_FEED_ID = "0x01584c4d2f55534400000000000000000000000000"  # XLM/USD feed ID

w3 = Web3(Web3.HTTPProvider(FLARE_RPC))

def log_price_fetch(source, price, success=True):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS" if success else "FAILED"
    msg = f"[{timestamp}] {source} fetch: {status} | Price: {price if success else 'None'}\n"
    print(msg.strip())
    try:
        with open("price_log.txt", 'a') as f:
            f.write(msg)
    except Exception:
        print("Price log write failed")

def fetch_from_ftso():
    try:
        ftso_v2_abi = [
            {"constant":True,"inputs":[{"name":"feedId","type":"bytes21"}],"name":"getFeedById","outputs":[{"name":"value","type":"uint256"},{"name":"decimals","type":"int8"},{"name":"timestamp","type":"uint64"}],"type":"function"}
        ]
        contract = w3.eth.contract(address=FTSO_V2_ADDRESS, abi=ftso_v2_abi)
        feed_id_bytes = bytes.fromhex(XLM_USD_FEED_ID[2:])
        result = contract.functions.getFeedById(feed_id_bytes).call()
        value, decimals, _ = result
        price = value / (10 ** decimals)
        log_price_fetch("FTSO", price)
        return price
    except Exception as e:
        log_price_fetch("FTSO", None, False)
        print(f"FTSO error: {str(e)}")
        return None

def fetch_from_mexc():
    try:
        exchange = ccxt.mexc({'enableRateLimit': True, 'timeout': 8000})
        ticker = exchange.fetch_ticker(SYMBOL)
        price = ticker['last']
        log_price_fetch("MEXC", price)
        return price
    except Exception as e:
        log_price_fetch("MEXC", None, False)
        print(f"MEXC error: {str(e)}")
        return None

def fetch_from_binance():
    try:
        exchange = ccxt.binance({'enableRateLimit': True, 'timeout': 8000})
        ticker = exchange.fetch_ticker(SYMBOL)
        price = ticker['last']
        log_price_fetch("Binance", price)
        return price
    except Exception as e:
        log_price_fetch("Binance", None, False)
        print(f"Binance error: {str(e)}")
        return None

def fetch_from_coingecko():
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={COINGECKO_ID}&vs_currencies={COINGECKO_VS}"
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        price = r.json().get(COINGECKO_ID, {}).get(COINGECKO_VS)
        if price:
            log_price_fetch("CoinGecko", price)
            return price
        log_price_fetch("CoinGecko", None, False)
        return None
    except Exception as e:
        log_price_fetch("CoinGecko", None, False)
        print(f"CoinGecko error: {str(e)}")
        return None

def get_current_xlm_price():
    price = fetch_from_ftso()
    if price is not None:
        return price

    price = fetch_from_mexc()
    if price is not None:
        return price

    price = fetch_from_binance()
    if price is not None:
        return price

    price = fetch_from_coingecko()
    if price is not None:
        return price

    print("Full blanket failed - check RPC/network/API")
    return None

# Nitro test
if __name__ == "__main__":
    print("=== Lambo™ Nitro Price Fetch v2.1 - FTSO Primary Blanket ===")
    for _ in range(3):
        price = get_current_xlm_price()
        print(f"XLM price: ${price if price else 'FAILED'}")
        if price is not None:
            break
        time.sleep(3)
    print("Logs in price_log.txt - FTSO should lead if RPC good")

# --- Lambo paste end ---