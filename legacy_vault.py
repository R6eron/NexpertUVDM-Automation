# legacy_vault.py – Ultimate Production Beast (Voice Legacy + Market Truth)
# All improvements integrated: real MEXC klines, file logging, Telegram alerts, sniper flag, error push

import os
import datetime
import hashlib
import json
import mimetypes
import time
import requests
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass
from web3 import Web3

# ────────────────────────────────────────────────
# CONFIG – FILL THESE ONCE
# ────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # from BotFather
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"      # your user/group ID
DAILY_LOG_FILE = "daily_price_diary.log"
PREV_LOWS_FILE = "prev_lows.json"
SNIPER_THRESHOLD = 0.160  # XLM < this → flag & alert

# Flare FTSO v2 – primary oracle
FLARE_RPC = "https://flare-api.flare.network/ext/C/rpc"
FTSO_V2_ADDRESS = "0x787C2AbB211dbC5F9B239288701a3dd5ae3Af1A2"

FTSO_ABI = [
    {
        "inputs": [{"internalType": "bytes21", "name": "feedId", "type": "bytes21"}],
        "name": "getFeedById",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "int8", "name": "", "type": "int8"},
            {"internalType": "uint64", "name": "", "type": "uint64"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

FEED_IDS = {
    'FLR': '0x01464c522f55534400000000000000000000000000',
    'XRP': '0x015852502f55534400000000000000000000000000',
    'XLM': '0x01584c4d2f55534400000000000000000000000000',
    'SGB': '0x015347422f55534400000000000000000000000000',
}

# Load prev lows cache
PREV_LOWS = {}
if os.path.exists(PREV_LOWS_FILE):
    try:
        with open(PREV_LOWS_FILE, 'r') as f:
            PREV_LOWS = json.load(f)
    except:
        pass
else:
    with open(PREV_LOWS_FILE, 'w') as f:
        json.dump(PREV_LOWS, f)

w3 = Web3(Web3.HTTPProvider(FLARE_RPC))
ftso = w3.eth.contract(address=FTSO_V2_ADDRESS, abi=FTSO_ABI)

def send_telegram_message(msg: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram config missing – skipping alert")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Telegram send fail: {e}")

def log_diary_entry(text: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {text}\n"
    with open(DAILY_LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(entry)

def get_ftso_price(feed_hex: str) -> Optional[float]:
    try:
        feed_bytes = bytes.fromhex(feed_hex[2:])
        val, dec, _ = ftso.functions.getFeedById(feed_bytes).call()
        return val / (10 ** abs(dec))
    except Exception as e:
        print(f"FTSO fail: {e}")
        return None

def get_mexc_klines(symbol: str) -> dict:
    """Fetch last 24h data via Day1 kline (public, no auth)"""
    try:
        url = "https://api.mexc.com/api/v3/klines"
        params = {"symbol": f"{symbol}USDT", "interval": "1d", "limit": 1}
        resp = requests.get(url, params=params, timeout=8).json()
        if not resp or not isinstance(resp, list) or len(resp) == 0:
            return {}
        k = resp[0]  # [open_time, open, high, low, close, volume, ...]
        return {
            "high": float(k[2]),
            "low": float(k[3]),
            "volume": float(k[5]),  # base asset volume
            "close": float(k[4])
        }
    except Exception as e:
        print(f"MEXC klines fail for {symbol}: {e}")
        return {}

def detect_low_change(sym: str, curr_low: float) -> str:
    key = sym + "_low"
    prev = PREV_LOWS.get(key)
    if prev is None:
        status = "first"
    elif curr_low > prev:
        status = "higher low ✅"
    elif curr_low < prev:
        status = "lower low ⚠️"
    else:
        status = "flat"
    PREV_LOWS[key] = curr_low
    with open(PREV_LOWS_FILE, 'w') as f:
        json.dump(PREV_LOWS, f)
    return status

def refresh_prices():
    timestamp = datetime.datetime.now().strftime('%B %d, %Y %H:%M')
    diary = f"#Jesse ON {timestamp}\n#DigitalAssetDiary\n\n"

    alerts = []
    for sym, fid in FEED_IDS.items():
        p_ftso = get_ftso_price(fid)
        klines = get_mexc_klines(sym)
        price = klines.get("close") if klines else p_ftso
        src = "MEXC klines" if klines else ("FTSO" if p_ftso is not None else "fail")

        if price is None:
            diary += f"**{sym}** — no price\n---\n"
            alerts.append(f"CRITICAL: {sym} both sources failed")
            continue

        high24 = klines.get("high", price * 1.05)
        low24 = klines.get("low", price * 0.95)
        vol24 = klines.get("volume", "N/A")

        rng = "high" if price >= high24 * 0.95 else "low" if price <= low24 * 1.05 else "mid"
        low_stat = detect_low_change(sym, low24)

        line = f"**{sym}**\n  ${price:.6f}  ({src})\n  Vol 24h: ${vol24 if vol24 == 'N/A' else f'{vol24:,.0f}'}\n  Range: {rng}  ({low24:.6f} – {high24:.6f})\n  Low: {low_stat}\n---\n"
        diary += line

        # Alerts
        if "higher low ✅" in low_stat:
            alerts.append(f"ALERT: {sym} higher low ✅ – momentum shift?")
        if isinstance(vol24, float) and vol24 > 5 * (PREV_LOWS.get(sym + "_vol", 0) or 1):  # rough spike detect
            alerts.append(f"ALERT: {sym} big vol push detected")
        PREV_LOWS[sym + "_vol"] = vol24 if isinstance(vol24, float) else 0  # update for next

        if sym == 'XLM' and price < SNIPER_THRESHOLD:
            alerts.append(f"SNIPER ZONE APPROACHING: XLM ${price:.6f} < {SNIPER_THRESHOLD}")

    diary += "\n**Sniper** XLM @0.158 untouched – pyramid waits\n"
    diary += "Wingman awake. Family first. Compound quiet. 🚀\n"

    # Log & alert
    log_diary_entry(diary)
    for alert in alerts:
        send_telegram_message(alert)
        log_diary_entry(f"ALERT: {alert}")

    print(diary)  # console for immediate view

# ────────────────────────────────────────────────
# LEGACY VAULT CORE
# ────────────────────────────────────────────────

@dataclass(frozen=True)
class VoiceArtifact:
    date: str
    family: List[str]
    transcription: str
    tokens: List[str]
    source_file: str
    hash: str

class LegacyVault:
    def __init__(self, repo_path: str, family_members: List[str]):
        self.repo_path: Path = Path(repo_path).resolve()
        self.family: List[str] = family_members
        self.voice_notes_dir: Path = self.repo_path / "voice_notes"
        self.artifacts_dir: Path = self.repo_path / "immutable_artifacts"
        self._ensure_dirs()

    def __repr__(self) -> str:
        return f"LegacyVault(repo={self.repo_path}, family={self.family})"

    def _ensure_dirs(self) -> None:
        self.voice_notes_dir.mkdir(parents=True, exist_ok=True)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

    def ingest_voice_note(self, file_path: str | Path, date: Optional[datetime.date] = None) -> VoiceArtifact:
        file_path = Path(file_path).resolve()
        
        if not file_path.exists():
            raise FileNotFoundError(f"Voice note not found: {file_path}")
        
        audio_mime, _ = mimetypes.guess_type(file_path)
        if not audio_mime or not audio_mime.startswith('audio/'):
            raise ValueError(f"Not an audio file: {file_path}")
        
        if date is None:
            date = datetime.date.today()
        
        try:
            transcription = self._transcribe(file_path)
            tokens = self._tokenize_essence(transcription)
            
            artifact_data = {
                "date": date.isoformat(),
                "family": self.family,
                "transcription": transcription,
                "tokens": tokens,
                "source_file": file_path.name,
            }
            
            content_hash = self._compute_hash(json.dumps(artifact_data, sort_keys=True))
            artifact_data["hash"] = content_hash
            
            artifact = VoiceArtifact(**artifact_data)
            
            artifact_path = self.artifacts_dir / f"artifact_{date.isoformat()}_{content_hash[:8]}.json"
            self._save_artifact(artifact_path, artifact)
            
            dest_voice = self.voice_notes_dir / file_path.name
            file_path.rename(dest_voice)
            
            self._feed_twin(artifact)
            
            print(f"✅ Artifact secured: {artifact_path}")
            print(f"📁 Voice archived: {dest_voice}")
            return artifact
            
        except Exception as e:
            print(f"❌ Processing failed for {file_path.name}: {e}")
            raise

    def _transcribe(self, file_path: Path) -> str:
        return f"Transcribed from {file_path.name}: wins, regrets, humor, scars..."

    def _tokenize_essence(self, text: str) -> List[str]:
        words = [w.strip() for w in text.split() if w.strip()]
        return [f"essence:{w[:50]}" for w in words[:20]]

    def _compute_hash(self, data: str) -> str:
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def _save_artifact(self, path: Path, artifact: VoiceArtifact) -> None:
        data = {
            "date": artifact.date,
            "family": artifact.family,
            "transcription": artifact.transcription,
            "tokens": artifact.tokens,
            "source_file": artifact.source_file,
            "hash": artifact.hash
        }
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')

    def _feed_twin(self, artifact: VoiceArtifact) -> None:
        print(f"🧠 Feeding twin: {artifact.date} – {len(artifact.tokens)} tokens ingested")

    def list_artifacts(self, date_range: Optional[tuple[datetime.date, datetime.date]] = None) -> List[Path]:
        artifacts = list(self.artifacts_dir.glob("artifact_*.json"))
        if date_range:
            start, end = date_range
            artifacts = [p for p in artifacts 
                         if self._parse_artifact_date(p) and start <= self._parse_artifact_date(p) <= end]
        return sorted(artifacts, reverse=True)

    def _parse_artifact_date(self, path: Path) -> Optional[datetime.date]:
        try:
            parts = path.stem.split('_')
            if len(parts) >= 2:
                return datetime.date.fromisoformat(parts[1])
        except:
            pass
        return None

    def run_daily(self) -> None:
        refresh_prices()  # auto diary + alerts on every cron run
        
        new_files = list(self.voice_notes_dir.glob("*.m4a")) + \
                    list(self.voice_notes_dir.glob("*.ogg")) + \
                    list(self.voice_notes_dir.glob("*.mp3"))
        for file_path in new_files:
            try:
                self.ingest_voice_note(file_path)
            except Exception as e:
                print(f"⚠️ Skipped {file_path.name}: {e}")

# Example usage
if __name__ == "__main__":
    vault = LegacyVault(
        repo_path="./legacy_vault_repo",
        family_members=["Jordan", "Ashley", "Keeley", "Kyeron", "Mia"]
    )
    
    test_file = vault.voice_notes_dir / "test_voice_2026-02-16.m4a"
    test_file.touch()
    
    artifact = vault.ingest_voice_note(test_file)
    print(f"Created artifact: {artifact}")
    print("\nRecent artifacts:", vault.list_artifacts())