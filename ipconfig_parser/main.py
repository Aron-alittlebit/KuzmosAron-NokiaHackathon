import sys
import json
from pathlib import Path

from Config import ENCODINGS, OUTPUT_FIELDS, LIST_FIELDS
from Parser import parse_file

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "output.json"


def read_file(path: Path) -> str:
    for enc in ENCODINGS:
        try:
            return path.read_text(encoding=enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def trim_adapter(adapter: dict) -> dict:
    result = {}
    for field in OUTPUT_FIELDS:
        val = adapter.get(field, "")
        result[field] = val if isinstance(val, list) else (val or "")
    return result


def process_file(path: Path) -> dict:
    adapters = parse_file(read_file(path))
    return {
        "file_name": path.name,
        "adapters": [trim_adapter(a) for a in adapters],
    }


def main():
    txt_files = sorted(BASE_DIR.rglob("*.txt"), key=lambda f: f.name)
    records = [process_file(f) for f in txt_files]

    output = json.dumps(records, indent=2, ensure_ascii=False)
    print(output)
    OUTPUT_FILE.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()