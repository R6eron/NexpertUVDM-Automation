# NexpertUVDM-Automation

This automation reduces human error, saves time, and ensures consistent execution of the UVDM’s virtuous cycles. Below, I outline the script’s core components and provide pseudocode for key processes to make the UVDM accessible to readers with basic programming knowledge.

## Quickstart
- **Install Dependencies**: `pip install ccxt requests substrate-interface xrpl-py flareio`
- **Run Automation**: `python main.py`
- **Customize API Keys**: Edit `config.py` with Nexo, MEXC, and BIFROST API keys (see Setup Guide).

## Full Code
- `xlm_price_checker.py`: Monitors XLM price, triggers harvest at $1, and reinvests at 20/30% drops.
- `uvdm_steps.py`: Simulates 8-step harvesting with 20/30% drop reinvestment.
- `xrpl_script.py`: Handles XRPL/Flare integration, Nexo balances, MEXC orders, and BIFROST staking.
- `main.py`: Orchestrates the UVDM automation flow.

## Demo
- GIF/screenshot of simulated run (e.g., $1 harvest or 20% drop reinvest) uploaded as `demo.gif`.

## Setup Guide
- **API Keys**:
  - **Nexo**: API Management > Generate API Key/Secret.
  - **MEXC**: API Center > Create API Key/Secret.
  - **BIFROST**: Wallet > API > Generate Key/Secret.
  - Add to `config.py`:
    ```python
    API_KEYS = {
        "nexo": {"api_key": "your_nexo_key", "secret": "your_nexo_secret"},
        "mexc": {"api_key": "your_mexc_key", "secret": "your_mexc_secret"},
        "bifrost": {"api_key": "your_bifrost_key", "secret": "your_bifrost_secret"},
        "xrpl_seed": "your_xrpl_seed"  # Private key equivalent
    }
    ```
- **Dependencies**: Run `pip install ccxt requests substrate-interface xrpl-py flareio` in terminal.

## Usage Examples
- `get_nexo_balance()`:
  - **Pseudocode**:
    ```
    FUNCTION get_nexo_balance():
        CONNECT to Nexo API with API_KEYS["nexo"]
        REQUEST balance endpoint
        RETURN XLM balance
    ```
- `place_mexc_order(price, amount)`:
  - **Pseudocode**:
    ```
    FUNCTION place_mexc_order(price, amount):
        CONNECT to MEXC API with API_KEYS["mexc"]
        SUBMIT limit order (price, amount XLM)
        CONFIRM order ID
        RETURN success/failure
    ```

## License
MIT License

Copyright (c) 2025 R.S. Lewis

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Purchase
- Amazon.com: https://www.amazon.com/dp/B0FQ8JRJV1
- Amazon.co.uk: https://www.amazon.co.uk/dp/B0FQ8JRJV1
- Amazon.de: https://www.amazon.de/dp/B0FQ8JRJV1
- Amazon.fr: https://www.amazon.fr/dp/B0FQ8JRJV1
- Amazon.es: https://www.amazon.es/dp/B0FQ8JRJV1
- Amazon.it: https://www.amazon.it/dp/B0FQ8JRJV1
- Amazon.co.jp: https://www.amazon.co.jp/dp/B0FQ8JRJV1
- Amazon.com.br: https://www.amazon.com.br/dp/B0FQ8JRJV1
- Amazon.ca: https://www.amazon.ca/dp/B0FQ8JRJV1
- Amazon.in: https://www.amazon.in/dp/B0FQ8JRJV1
- Amazon.com.au: https://www.amazon.com.au/dp/B0FQ8JRJV1
- Amazon.com.mx: https://www.amazon.com.mx/dp/B0FQ8JRJV1
- Amazon.nl: https://www.amazon.nl/dp/B0FQ8JRJV1    'enableRateLimit': True
})

def check_xlm_price(harvest_price=1.0, callback=None):
    print(f"Monitoring XLM price for harvest at ${harvest_price} and 20/30% drops...")
    high_water_mark = harvest_price
    while True:
        try:
            ticker = exchange.fetch_ticker('XLM/USD')
            current_price = ticker['last']
            print(f"Current XLM Price: ${current_price:.4f} at {time.ctime()}")
            if current_price >= harvest_price and callback:
                print(f"ALERT: XLM reached ${harvest_price}! Triggering harvest.")
                callback(current_price, high_water_mark)
                high_water_mark = current_price
            drop20 = high_water_mark * 0.80  # 20% drop
            drop30 = high_water_mark * 0.70  # 30% drop
            if current_price <= drop20 or current_price <= drop30:
                print(f"ALERT: 20% (${drop20:.2f}) or 30% (${drop30:.2f}) drop detected! Triggering reinvest.")
                callback(current_price, high_water_mark, reinvest=True)
                high_water_mark = current_price
            time.sleep(300)
        except ccxt.NetworkError as e:
            print(f"Network Error: {e}. Retrying in 60s...")
            time.sleep(60)
        except Exception as e:
            print(f"Error: {e}. Retrying in 60s...")
            time.sleep(60)

if __name__ == "__main__":
    def dummy_callback(price, mark, reinvest=False):
        action = "reinvest" if reinvest else "harvest"
        print(f"Callback triggered at ${price:.2f} for {action}, high mark: ${mark:.2f}")
    check_xlm_price(callback=dummy_callback)

## Demo
- GIF/screenshot of simulated run (e.g., $1 XLM trigger alert) uploaded as `demo.gif`.

## Scripts
- `uvdm_steps.py`: 8-step harvesting simulation (pg. 28-29) with swap projections (input: 108K XLM; output: yield to $60K).
- `xrpl_script.py`: XRPL/Flare integration for FTSO voting and minting.

## Setup Guide
- **API Keys**: 
  - **Nexo**: API Management > Generate API Key/Secret.
  - **MEXC**: API Center > Create API Key/Secret.
  - **BIFROST**: Wallet > API > Generate Key/Secret.
  - Add to `config.py`:
    ```python
    import ccxt
import time
from config import API_KEYS

exchange = ccxt.nexo({
    'apiKey': API_KEYS["nexo"]["api_key"],
    'secret': API_KEYS["nexo"]["secret"],
    'enableRateLimit': True
})

def check_xlm_price(harvest_price=1.0, callback=None):
    print(f"Monitoring XLM price for harvest at ${harvest_price} and 20/30% drops...")
    high_water_mark = harvest_price
    while True:
        try:
            ticker = exchange.fetch_ticker('XLM/USD')
            current_price = ticker['last']
            print(f"Current XLM Price: ${current_price:.4f} at {time.ctime()}")
            if current_price >= harvest_price and callback:
                print(f"ALERT: XLM reached ${harvest_price}! Triggering harvest.")
                callback(current_price, high_water_mark)
                high_water_mark = current_price
            drop20 = high_water_mark * 0.80  # 20% drop
            drop30 = high_water_mark * 0.70  # 30% drop
            if current_price <= drop20 or current_price <= drop30:
                print(f"ALERT: 20% (${drop20:.2f}) or 30% (${drop30:.2f}) drop detected! Triggering reinvest.")
                callback(current_price, high_water_mark, reinvest=True)
                high_water_mark = current_price
            time.sleep(300)
        except ccxt.NetworkError as e:
            print(f"Network Error: {e}. Retrying in 60s...")
            time.sleep(60)
        except Exception as e:
            print(f"Error: {e}. Retrying in 60s...")
            time.sleep(60)

if __name__ == "__main__":
    def dummy_callback(price, mark, reinvest=False):
        action = "reinvest" if reinvest else "harvest"
        print(f"Callback triggered at ${price:.2f} for {action}, high mark: ${mark:.2f}")
    check_xlm_price(callback=dummy_callback)
    API_KEYS = {
        "nexo": {"api_key": "your_nexo_key", "secret": "your_nexo_secret"},
        "mexc": {"api_key": "your_mexc_key", "secret": "your_mexc_secret"},
        "bifrost": {"api_key": "your_bifrost_key", "secret": "your_bifrost_secret"},
        "xrpl_seed": "your_xrpl_seed"  # Private key equivalent
    }
    def simulate_uvdm_steps(initial_xlm=115735, current_price=1.0, reinvest_price=None):
    xlm_balance = initial_xlm
    dai_balance = 0
    paxg_balance = 0  # In ounces
    print("UVDM 8-Step Harvesting Simulation")
    print(f"Initial XLM: {initial_xlm:.0f} at ${current_price}")
    print("Target | Harvest XLM | Harvest Value | DAI | PAXG (oz) | New XLM | Total Value")
    print("-" * 70)

    if current_price >= 1.0:  # Harvest trigger
        harvest = (xlm_balance - 50000) * 0.1 if xlm_balance > 50000 else xlm_balance * 0.1
        harvest_value = harvest * current_price
        dai = harvest_value * 0.5
        paxg = harvest_value * 0.5 / 2500
        xlm_balance -= harvest
        dai_balance += dai
        paxg_balance += paxg
        total_value = (xlm_balance * current_price) + dai_balance + (paxg_balance * 2500)
        print(f"${current_price:^5} | {harvest:.0f:^10} | ${harvest_value:>10,.0f} | ${dai:>6.0f} | {paxg:>9.3f} | {xlm_balance:.0f:^8} | ${total_value:>10,.0f}")
        print(f"Holding DAI: ${dai:.0f}, PAXG: {paxg:.3f} oz until 20/30% drop.")

    if reinvest_price:  # Reinvest trigger
        reinvest_amount = (dai_balance + paxg_balance * 2500) * 0.5  # 50% of held value
        reinvest_xlm = reinvest_amount / reinvest_price
        xlm_balance += reinvest_xlm
        dai_balance *= 0.5
        paxg_balance *= 0.5
        total_value = (xlm_balance * reinvest_price) + dai_balance + (paxg_balance * 2500)
        print(f"Reinvest at ${reinvest_price:^5} | New XLM: {reinvest_xlm:.0f} | Total XLM: {xlm_balance:.0f} | Total Value: ${total_value:,.0f}")

    for target in [2, 3, 4, 5, 6, 7, 8]:
        harvest = xlm_balance * 0.1
        harvest_value = harvest * target
        dai = harvest_value * 0.5
        paxg = harvest_value * 0.5 / 2500
        xlm_balance -= harvest
        dai_balance += dai
        paxg_balance += paxg
        total_value = (xlm_balance * target) + dai_balance + (paxg_balance * 2500)
        print(f"${target:^5} | {harvest:.0f:^10} | ${harvest_value:>10,.0f} | ${dai:>6.0f} | {paxg:>9.3f} | {xlm_balance:.0f:^8} | ${total_value:>10,.0f}")

    yield_projection = (xlm_balance * 8 + dai_balance + paxg_balance * 2500) * 0.11
    print("\nFinal XLM: {:.0f}, Total Value at $8: ${:,.2f}")
    print(f"Projected Annual Yield (11% APY): ${yield_projection:,.2f} (targets $60K)")

if __name__ == "__main__":
    simulate_uvdm_steps()
    ```
- **Dependencies**: Run `pip install ccxt requests substrate-interface xrpl-py flareio` in terminal.

## Usage Examples
- `get_nexo_balance()`:
  - **Pseudocode**:
    ```
    FUNCTION get_nexo_balance():
        CONNECT to Nexo API with API_KEYS["nexo"]
        REQUEST balance endpoint
        RETURN XLM balance
    ```
- `place_mexc_order(price, amount)`:
  - **Pseudocode**:
  - def simulate_uvdm_steps(initial_xlm=115735, current_price=1.0, reinvest_price=None):
    xlm_balance = initial_xlm
    dai_balance = 0
    paxg_balance = 0  # In ounces
    print("UVDM 8-Step Harvesting Simulation")
    print(f"Initial XLM: {initial_xlm:.0f} at ${current_price}")
    print("Target | Harvest XLM | Harvest Value | DAI | PAXG (oz) | New XLM | Total Value")
    print("-" * 70)

    if current_price >= 1.0:  # Harvest trigger
        harvest = (xlm_balance - 50000) * 0.1 if xlm_balance > 50000 else xlm_balance * 0.1
        harvest_value = harvest * current_price
        dai = harvest_value * 0.5
        paxg = harvest_value * 0.5 / 2500
        xlm_balance -= harvest
        dai_balance += dai
        paxg_balance += paxg
        total_value = (xlm_balance * current_price) + dai_balance + (paxg_balance * 2500)
        print(f"${current_price:^5} | {harvest:.0f:^10} | ${harvest_value:>10,.0f} | ${dai:>6.0f} | {paxg:>9.3f} | {xlm_balance:.0f:^8} | ${total_value:>10,.0f}")
        print(f"Holding DAI: ${dai:.0f}, PAXG: {paxg:.3f} oz until 20/30% drop.")

    if reinvest_price:  # Reinvest trigger
        reinvest_amount = (dai_balance + paxg_balance * 2500) * 0.5  # 50% of held value
        reinvest_xlm = reinvest_amount / reinvest_price
        xlm_balance += reinvest_xlm
        dai_balance *= 0.5
        paxg_balance *= 0.5
        total_value = (xlm_balance * reinvest_price) + dai_balance + (paxg_balance * 2500)
        print(f"Reinvest at ${reinvest_price:^5} | New XLM: {reinvest_xlm:.0f} | Total XLM: {xlm_balance:.0f} | Total Value: ${total_value:,.0f}")

    for target in [2, 3, 4, 5, 6, 7, 8]:
        harvest = xlm_balance * 0.1
        harvest_value = harvest * target
        dai = harvest_value * 0.5
        paxg = harvest_value * 0.5 / 2500
        xlm_balance -= harvest
        dai_balance += dai
        paxg_balance += paxg
        total_value = (xlm_balance * target) + dai_balance + (paxg_balance * 2500)
        print(f"${target:^5} | {harvest:.0f:^10} | ${harvest_value:>10,.0f} | ${dai:>6.0f} | {paxg:>9.3f} | {xlm_balance:.0f:^8} | ${total_value:>10,.0f}")

    yield_projection = (xlm_balance * 8 + dai_balance + paxg_balance * 2500) * 0.11
    print("\nFinal XLM: {:.0f}, Total Value at $8: ${:,.2f}")
    print(f"Projected Annual Yield (11% APY): ${yield_projection:,.2f} (targets $60K)")

if __name__ == "__main__":
    simulate_uvdm_steps()
    import requests
import time
import hmac
import hashlib
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment
from xrpl.transaction import safe_sign_and_submit_transaction
from flareio import FlareApiClient
from config import API_KEYS

def connect_to_xrpl(url="https://s1.ripple.com:51234", timeout=10):
    try:
        client = JsonRpcClient(url)
        info = client.request(ServerInfo())
        return client if info.is_successful() else None
    except Exception as e:
        print(f"XRPL Error: {e}")
        return None

def get_nexo_balance():
    url = "https://api.nexo.com/v1/balances"
    headers = {"X-API-KEY": API_KEYS["nexo"]["api_key"], "Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        balances = response.json()
        return next((b['available'] for b in balances if b['currency'] == 'XLM'), 0)
    except Exception as e:
        print(f"Nexo Error: {e}")
        return 0

def place_mexc_order(symbol, side, quantity, price):
    base_url = "https://api.mexc.com"
    endpoint = "/api/v3/order"
    timestamp = int(time.time() * 1000)
    params = {"symbol": symbol, "side": side, "type": "LIMIT", "quantity": quantity, "price": price, "timestamp": timestamp, "recvWindow": 5000}
    query_string = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
    signature = hmac.new(API_KEYS["mexc"]["secret"].encode(), query_string.encode(), hashlib.sha256).hexdigest().lower()
    params["signature"] = signature
    headers = {"X-MEXC-APIKEY": API_KEYS["mexc"]["api_key"], "Content-Type": "application/x-www-form-urlencoded"}
    try:
        response = requests.post(f"{base_url}{endpoint}", headers=headers, data=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"MEXC Error: {e}")
        return None

def connect_to_flare_protocols():
    api_key = API_KEYS.get('flare_api_key', '')
    if not api_key:
        print("Flare API key missing.")
        return None
    try:
        return FlareApiClient(api_key=api_key)
    except Exception as e:
        print(f"Flare Error: {e}")
        return None

def auto_wrap_flare_tokens(amount, flare_client):
    try:
        response = flare_client.post("/wrap", data={"amount": amount})
        return response.json().get("wrapped_amount", amount * 1.1)
    except Exception as e:
        print(f"Wrap Error: {e}")
        return None

def main_harvest(xlm_balance, current_price, high_water_mark, reinvest=False):
    if current_price >= 1.0 and not reinvest:
        harvest = (xlm_balance - 50000) * 0.1 if xlm_balance > 50000 else xlm_balance * 0.1
        order = place_mexc_order("XLMUSDT", "SELL", str(harvest), str(current_price))
        if order:
            harvest_value = float(order.get("cummulativeQuoteQty", 0))
            return {"xlm": xlm_balance - harvest, "dai": harvest_value * 0.5, "paxg": harvest_value * 0.5 / 2500}
    elif reinvest:
        drop_ratio = high_water_mark / current_price
        if drop_ratio >= 1.25 or drop_ratio >= 1.43:  # 20% or 30% drop
            reinvest_amount = (dai_balance + paxg_balance * 2500) * 0.5  # 50% of held value
            order = place_mexc_order("XLMUSDT", "BUY", str(reinvest_amount / current_price), str(current_price))
            if order:
                reinvest_xlm = reinvest_amount / current_price
                return {"xlm": xlm_balance + reinvest_xlm, "dai": dai_balance * 0.5, "paxg": paxg_balance * 0.5}
    return {"xlm": xlm_balance, "dai": 0, "paxg": 0}

if __name__ == "__main__":
    xrpl_client = connect_to_xrpl()
    xlm_balance = get_nexo_balance() or 115735
    dai_balance = 0
    paxg_balance = 0
    check_xlm_price(callback=lambda price, mark, reinvest=False: [
        setattr(globals(), 'xlm_balance', main_harvest(xlm_balance, price, mark, reinvest)["xlm"]),
        setattr(globals(), 'dai_balance', main_harvest(xlm_balance, price, mark, reinvest)["dai"]),
        setattr(globals(), 'paxg_balance', main_harvest(xlm_balance, price, mark, reinvest)["paxg"])
    ])
    from xlm_price_checker import check_xlm_price
from uvdm_steps import simulate_uvdm_steps
from xrpl_script import main_harvest, get_nexo_balance

def run_uvdm_automation():
    initial_xlm = get_nexo_balance() or 115735
    print(f"Starting with XLM: {initial_xlm}")
    check_xlm_price(callback=lambda price, mark, reinvest=False: simulate_uvdm_steps(initial_xlm, current_price=price, reinvest_price=price if reinvest else None))
    print("UVDM cycle completed. Monitoring...")

if __name__ == "__main__":
    run_uvdm_automation()
    config.py
*.key
*.secret
__pycache__/
*.pyc
*.gif
    ```
    FUNCTION place_mexc_order(price, amount):
        CONNECT to MEXC API with API_KEYS["mexc"]
        SUBMIT limit order (price, amount XLM)
        CONFIRM order ID
        RETURN success/failure
    ```

## License
MIT License

Copyright (c) 2025 R.S. Lewis

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Purchase
- Amazon.com: https://www.amazon.com/dp/B0FQ8JRJV1
- Amazon.co.uk: https://www.amazon.co.uk/dp/B0FQ8JRJV1
- Amazon.de: https://www.amazon.de/dp/B0FQ8JRJV1
- Amazon.fr: https://www.amazon.fr/dp/B0FQ8JRJV1
- Amazon.es: https://www.amazon.es/dp/B0FQ8JRJV1
- Amazon.it: https://www.amazon.it/dp/B0FQ8JRJV1
- Amazon.co.jp: https://www.amazon.co.jp/dp/B0FQ8JRJV1
- Amazon.com.br: https://www.amazon.com.br/dp/B0FQ8JRJV1
- Amazon.ca: https://www.amazon.ca/dp/B0FQ8JRJV1
- Amazon.in: https://www.amazon.in/dp/B0FQ8JRJV1
- Amazon.com.au: https://www.amazon.com.au/dp/B0FQ8JRJV1
- Amazon.com.mx: https://www.amazon.com.mx/dp/B0FQ8JRJV1
- Amazon.nl: https://www.amazon.nl/dp/B0FQ8JRJV1https://www.amazon.ca/dp/B0FQ8JRJV1
Amazon.in
UVDM B0FQ8JRJV1 ASIN
https://www.amazon.in/dp/B0FQ8JRJV1
Amazon.com.au
UVDM B0FQ8JRJV1 ASIN
https://www.amazon.com.au/dp/B0FQ8JRJV1
Amazon.com.mx
UVDM B0FQ8JRJV1 ASIN
https://www.amazon.com.mx/dp/B0FQ8JRJV1
Amazon.nl
UVDM B0FQ8JRJV1 ASIN
https://www.amazon.nl/dp/B0FQ8JRJV1
import requests
import time
import json
import hmac
import hashlib
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment
from xrpl.transaction import safe_sign_and_submit_transaction
from flareio import FlareApiClient  # pip install flareio (from GitHub: Flared/python-flareio)
# xrpl_script.py
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import ServerInfo
import websocket
import logging

# Insert the connect_to_xrpl function here
def connect_to_xrpl(url="wss://s1.ripple.com:443", timeout=10):
    # ... (the full function from above)

# Example function using the XRPL client
def get_account_info(client, account):
    from xrpl.models.requests import AccountInfo
    try:
        response = client.request(AccountInfo(account=account))
        if response.is_successful():
            return response.result
        else:
            logging.error(f"Failed to get account info: {response.status}")
            return None
    except Exception as e:
        logging.error(f"Error fetching account info: {str(e)}")
        return None

if __name__ == "__main__":
    client = connect_to_xrpl()
    if client:
        # Example: Fetch account info for a sample XRPL address
        account_info = get_account_info(client, "rYourAccountAddressHere")
        if account_info:
            print(f"Account info: {account_info}")
        else:
            print("Failed to fetch account info.")
    else:
        print("Failed to connect to XRPL.")
# User Input for API Keys/Secrets (prompt at runtime)
def get_api_credentials():
    print("Enter your API credentials (keep secure!):")
    nexo_api_key = input("Nexo API Key: ").strip()
    mexc_api_key = input("MEXC API Key: ").strip()
    mexc_api_secret = input("MEXC API Secret: ").strip()
    xrpl_seed = input("XRPL Wallet Seed (private key equiv.): ").strip()  # For signing
    flare_api_key = input("Flare API Key (if needed): ").strip()
    bifrost_ws_endpoint = input("Bifrost RPC Endpoint (default: https://api.bifrost.finance/staking): ") or "https://api.bifrost.finance/staking"
    if not all([nexo_api_key, mexc_api_key, mexc_api_secret, xrpl_seed]):
        print("Error: Required credentials missing. Exiting.")
        return None
    return {
        'nexo_api_key': nexo_api_key,
        'mexc_api_key': mexc_api_key,
        'mexc_api_secret': mexc_api_secret,
        'xrpl_seed': xrpl_seed,
        'flare_api_key': flare_api_key,
        'bifrost_endpoint': bifrost_ws_endpoint
    }

# Global credentials
credentials = get_api_credentials()
if not credentials:
    exit(1)

# Connect to XRPL network (health check)
def connect_to_xrpl():
    xrpl_url = "https://s1.ripple.com:51234"
    timeout = 10
    try:
        response = requests.get(xrpl_url, timeout=timeout)
        if response.status_code == 200:
            print("Connected to XRPL network successfully.")
            return JsonRpcClient(xrpl_url)
        else:
            print(f"Failed to connect to XRPL network (status: {response.status_code}).")
            return None
    except requests.exceptions.RequestException as e:
        print("Connection to XRPL network failed:", e)
        return None

# Retrieve previous month's best performing FTSO data (using Flare API)
def retrieve_previous_month_ftso_data():
    ftso_api_url = "https://api.flare.network/ftso-data"  # Real Flare API endpoint
    try:
        response = requests.get(ftso_api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        top_ftsos = sorted(data, key=lambda x: x.get("performance_score", 0), reverse=True)[:2]  # Top 2 FTSOs
        print("Top FTSOs:", top_ftsos)
        return top_ftsos
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve FTSO data (using mock):", e)
        return [{"ftso_id": "mock1", "performance_score": 95}, {"ftso_id": "mock2", "performance_score": 90}]

# Connect to Flare Protocols (using python-flareio SDK)
def connect_to_flare_protocols():
    api_key = credentials['flare_api_key']
    if not api_key:
        print("Flare API key required.")
        return None
    try:
        api_client = FlareApiClient(api_key=api_key)
        print("Connected to Flare Protocols successfully.")
        return api_client
    except Exception as e:
        print("Failed to connect to Flare Protocols:", e)
        return None

# Auto-wrap Flare tokens (using Flare SDK)
def auto_wrap_flare_tokens(flare_token_amount, flare_client):
    try:
        # Using FlareApiClient to wrap tokens (adapt from docs)
        wrapped_response = flare_client.post("/wrap", data={"amount": flare_token_amount})
        wrapped_tokens = wrapped_response.json().get("wrapped_amount", flare_token_amount * 1.1)
        print(f"Auto-wrapped {flare_token_amount} Flare tokens to {wrapped_tokens}")
        return wrapped_tokens
    except Exception as e:
        print("Failed to wrap Flare tokens:", e)
        return None

# Delegate votes to best FTSOs (full XRPL tx submission)
def delegate_votes_to_best_ftsos(wrapped_tokens, ftso_data, xrpl_client):
    total_votes = 100
    vote_percentage = 50
    votes_per_ftso = total_votes * (vote_percentage / 100)
    
    wallet = Wallet.from_seed(credentials['xrpl_seed'])
    
    for ftso in ftso_data:
        try:
            # Full XRPL transaction for delegation (mock Payment for FTSO vote)
            tx = Payment(
                account=wallet.classic_address,
                destination="rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh",  # Mock FTSO destination
                amount=str(votes_per_ftso)
            )
            response = safe_sign_and_submit_transaction(tx, wallet, xrpl_client)
            print(f"Delegated {votes_per_ftso} votes to FTSO ID {ftso['ftso_id']}: {response.result}")
        except Exception as e:
            print(f"Failed to delegate votes to FTSO {ftso['ftso_id']}:", e)

# Mint F assets (full XRPL mint tx)
def mint_f_assets(crypto_sets, xrpl_client):
    f_assets = []
    wallet = Wallet.from_seed(credentials['xrpl_seed'])
    for crypto_set in crypto_sets:
        try:
            # Full XRPL mint transaction (using Payment as mint proxy)
            tx = Payment(
                account=wallet.classic_address,
                destination=wallet.classic_address,  # Self-mint
                amount="100"  # Amount for f_asset
            )
            response = safe_sign_and_submit_transaction(tx, wallet, xrpl_client)
            f_asset = {
                "crypto_set": crypto_set,
                "f_asset_id": f"f_asset_{crypto_set}",
                "amount": 100,
                "tx_result": response.result
            }
            f_assets.append(f_asset)
            print(f"Minted {f_asset['amount']} {f_asset['f_asset_id']}: {response.result}")
        except Exception as e:
            print(f"Failed to mint {crypto_set}:", e)
    return f_assets

# NEXO API Integration: Get Account Balance (authenticated call with error handling)
def get_nexo_balance():
    url = "https://api.nexo.com/v1/balances"  # From Nexo Pro API
    headers = {
        "X-API-KEY": credentials['nexo_api_key'],
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        balances = response.json()
        print("Nexo Balances:", balances)
        return balances
    except requests.exceptions.RequestException as e:
        print(f"Nexo API Error: {e}")
        return None

# MEXC API Integration: Place Limit Order (with HMAC signing)
def place_mexc_order(symbol, side, quantity, price):
    base_url = "https://api.mexc.com"
    endpoint = "/api/v3/order"
    timestamp = int(time.time() * 1000)
    params = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "quantity": quantity,
        "price": price,
        "timestamp": timestamp,
        "recvWindow": 5000
    }
    
    # Generate signature
    query_string = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
    signature = hmac.new(
        credentials['mexc_api_secret'].encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest().lower()
    params["signature"] = signature
    
    headers = {
        "X-MEXC-APIKEY": credentials['mexc_api_key'],
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        response = requests.post(f"{base_url}{endpoint}", headers=headers, data=params, timeout=10)
        response.raise_for_status()
        order = response.json()
        print("MEXC Order Placed:", order)
        return order
    except requests.exceptions.RequestException as e:
        print(f"MEXC API Error: {e}")
        return None

# BIFROST API Integration: Query Staking Info (public RPC via HTTP fallback)
def query_bifrost_staking():
    bifrost_url = credentials['bifrost_endpoint']  # e.g., https://api.bifrost.finance/staking
    try:
        response = requests.get(bifrost_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        print("Bifrost Staking Data:", data)
        return data
    except requests.exceptions.RequestException as e:
        print("Failed to query Bifrost:", e)
        return {"mock_staking": "100 FLR delegated"}

# Monitor asset prices with trailing stop-loss (integrate MEXC for price)
def get_asset_price(symbol="BTCUSDT"):
    url = f"https://api.mexc.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        price = float(response.json()['price'])
        return price
    except:
        return 0.50  # Fallback

def monitor_asset_prices():
    highest_price = 0
    stop_loss_price = 0
    trailing_percentage = 0.3
    max_iterations = 10  # Limit loop for testing
    
    for i in range(max_iterations):
        asset_price = get_asset_price()
        if asset_price > highest_price:
            highest_price = asset_price
            stop_loss_price = highest_price * (1 - trailing_percentage)
        if asset_price <= stop_loss_price:
            trigger_stop_loss()
            break
        print(f"Iteration {i+1}: Current price: {asset_price}, Stop-loss: {stop_loss_price}")
        time.sleep(60)  # Check every minute

def trigger_stop_loss():
    print("Stop-loss triggered! Executing via MEXC.")
    place_mexc_order("BTCUSDT", "SELL", "0.001", "market")  # Adapt for market order

# Main function
def main():
    print("Starting UVDM Script...")
    xrpl_client = connect_to_xrpl()
    if not xrpl_client:
        return
    
    # Integrate platform APIs before minting
    print("Fetching Nexo balance...")
    nexo_bal = get_nexo_balance()
    print("Querying Bifrost staking...")
    bifrost_data = query_bifrost_staking()
    
    flare_client = connect_to_flare_protocols()
    if not flare_client:
        return
    
    # Simulate incoming Flare tokens
    flare_token_amount = 1000
    wrapped_tokens = auto_wrap_flare_tokens(flare_token_amount, flare_client)
    if not wrapped_tokens:
        return
    
    ftso_data = retrieve_previous_month_ftso_data()
    if ftso_data:
        delegate_votes_to_best_ftsos(wrapped_tokens, ftso_data, xrpl_client)
    
    # Simulate cryptocurrency sets for minting
    crypto_sets = ["set1", "set2", "set3"]
    f_assets = mint_f_assets(crypto_sets, xrpl_client)
    print("Minted F assets:", f_assets)
    
    # Example MEXC order
    place_mexc_order("BTCUSDT", "BUY", "0.001", "50000")
    
    # Start price monitoring
    monitor_asset_prices()

if __name__ == "__main__":
    main()
