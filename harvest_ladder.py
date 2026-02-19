# harvest_ladder.py - Lambo™ Nitro Edition: Complete Harvest Ladder Module
# Starts $1.00, +$0.50 rungs to $8.00, stateful, jump-safe, logging + sim balance
# 4-space indent, no trailing spaces, Termux/S20 paste-proof - ONE tested block

import json
import datetime

STATE_FILE = "harvest_state.json"
LOG_FILE = "harvest_log.txt"
INITIAL_XLM = 93000.0  # your \~93k spot bag sim

def load_last_harvested():
    try:
        with open(STATE_FILE, 'r') as f:
            data = json.load(f)
            return data.get("last_harvested", 0.99)
    except FileNotFoundError:
        return 0.99
    except Exception:
        return 0.99

def save_last_harvested(level):
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump({"last_harvested": level}, f)
    except Exception as e:
        print(f"State save failed: {e}")

def log_harvest(thresh, amount_sold, proceeds):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] XLM >= \( {thresh:.2f} | Sold {amount_sold:.2f} XLM | Proceeds \~ \){proceeds:.2f}\n"
    print(msg.strip())
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(msg)
    except Exception:
        print("Log write failed - check permissions")

def check_and_harvest(current_price, current_xlm_balance=INITIAL_XLM):
    if current_price is None or current_price < 1.00:
        return {"harvested": False, "details": None}

    thresholds = [
        1.00, 1.50, 2.00, 2.50, 3.00, 3.50, 4.00, 4.50, 5.00,
        5.50, 6.00, 6.50, 7.00, 7.50, 8.00
    ]

    last_harvested = load_last_harvested()
    sorted_thresh = sorted(thresholds, reverse=True)

    for thresh in sorted_thresh:
        if current_price >= thresh and thresh > last_harvested:
            sell_amount = current_xlm_balance * 0.10
            proceeds = sell_amount * current_price  # approx, ignore fees/slippage for sim
            log_harvest(thresh, sell_amount, proceeds)
            new_balance = current_xlm_balance - sell_amount
            save_last_harvested(thresh)
            return {
                "harvested": True,
                "details": {
                    "threshold": thresh,
                    "sold_xlm": sell_amount,
                    "proceeds_usd": proceeds,
                    "remaining_xlm": new_balance,
                    "timestamp": datetime.datetime.now().isoformat()
                }
            }

    return {"harvested": False, "details": None}

# Nitro self-test: realistic price path + balance decay
if __name__ == "__main__":
    print("=== Lambo™ Nitro Test Run ===")
    print(f"Starting sim balance: {INITIAL_XLM:.2f} XLM\n")

    test_sequence = [
        0.98, 1.02, 1.55, 1.80, 2.10, 2.40, 1.95, 3.20,
        4.10, 4.80, 5.30, 6.00, 7.20, 8.50  # overshoot to test cap
    ]

    balance = INITIAL_XLM
    for price in test_sequence:
        print(f"Price ${price:.2f} | Balance {balance:.2f} XLM")
        result = check_and_harvest(price, balance)
        if result["harvested"]:
            print(f"  HARVESTED at ${result['details']['threshold']:.2f}")
            print(f"  Sold {result['details']['sold_xlm']:.2f} XLM → \~${result['details']['proceeds_usd']:.2f}")
            balance = result['details']['remaining_xlm']
        else:
            print("  No action")
        print("---")

    print(f"\nFinal sim balance after harvests: {balance:.2f} XLM")
    print("Check harvest_log.txt & harvest_state.json for persistence")

# --- Lambo paste end ---