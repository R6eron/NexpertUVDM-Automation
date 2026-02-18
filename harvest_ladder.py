# harvest_ladder.py - Lambo™ Mobile Harvest Ladder Module
# Standalone: starts at $1.00, then +$0.50 intervals
# Stateful (json), jump-safe, 4-space indent, no trailing spaces
# Termux / cracked S20 paste-proof - one block only

import json

STATE_FILE = "harvest_state.json"

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

def check_and_harvest(current_price):
    if current_price is None or current_price < 1.00:
        return False

    thresholds = [
        1.00, 1.50, 2.00, 2.50, 3.00, 3.50, 4.00, 4.50, 5.00,
        5.50, 6.00, 6.50, 7.00, 7.50, 8.00
    ]

    last_harvested = load_last_harvested()
    sorted_thresh = sorted(thresholds, reverse=True)

    for thresh in sorted_thresh:
        if current_price >= thresh and thresh > last_harvested:
            print(f"XLM >= ${thresh:.2f} - NEW RUNG CROSSED - Harvest 10% → 50/50 DAI/PAXG")
            # TODO: Insert your real harvest/swap logic here
            # Example placeholder:
            # amount = get_xlm_balance() * 0.10
            # execute_swap(amount, 'XLM', split='50/50 DAI/PAXG')
            save_last_harvested(thresh)
            return True

    return False

# Quick self-test - run with python harvest_ladder.py
# Comment out the block below when integrating to main bot
if __name__ == "__main__":
    test_prices = [0.95, 1.03, 1.70, 2.40, 2.10, 3.80, 4.20, 7.90, 8.10]
    for p in test_prices:
        print(f"Price ${p:.2f}: ", end="")
        if check_and_harvest(p):
            print("HARVESTED")
        else:
            print("no action")
        print("---")

# --- Lambo paste end ---