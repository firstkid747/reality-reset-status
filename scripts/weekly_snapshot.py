import json, hashlib, os
from datetime import datetime, timezone

PUBLIC_DIR = "public"
LEDGER_PATH = os.path.join(PUBLIC_DIR, "ledger.jsonl")
SNAPSHOT_DIR = os.path.join(PUBLIC_DIR, "snapshots")

def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def main():
    if not os.path.exists(LEDGER_PATH):
        print("No ledger found.")
        return

    os.makedirs(SNAPSHOT_DIR, exist_ok=True)

    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        ledger = f.read()

    ts = datetime.now(timezone.utc).date().isoformat()
    snapshot_name = f"week_snapshot_{ts}.json"

    snapshot = {
        "snapshot_date": ts,
        "ledger_lines": ledger.count("\n"),
        "ledger_hash": sha256_text(ledger),
        "ledger": ledger.splitlines()
    }

    out_path = os.path.join(SNAPSHOT_DIR, snapshot_name)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)

    with open(os.path.join(SNAPSHOT_DIR, f"{snapshot_name}.hash.txt"), "w") as f:
        f.write(snapshot["ledger_hash"])

if __name__ == "__main__":
    main()