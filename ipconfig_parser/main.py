from pathlib import Path
from typing import Dict, Optional, List
import json


def sanitize_key(key: str) -> str:
    return key.replace(".", "").strip().lower().replace("-", "_").replace(" ", "_")


def parse_ipconfig(filename: str, raw_text: str) -> Dict[str, str | List[str]]:
    result = {"filename": filename, "adapters": []}
    current_adapter: Optional[Dict[str, str | List[str]]] = None
    last_key: Optional[str] = None

    for line in raw_text.splitlines():
        stripped = line.strip()

        if stripped == "":
            continue

        if not (line.startswith(" ") or line.startswith("\t")) and stripped.endswith(":"):
            if current_adapter is not None:
                result["adapters"].append(current_adapter)
            current_adapter = {"adapter_name": stripped[:-1]}
            continue

        if line.startswith(" ") or line.startswith("\t"):
            if current_adapter is None:
                current_adapter = {"adapter_name": ""}

            if last_key is not None and ":" not in stripped:
                if type(current_adapter[last_key]) == str:
                    current_adapter[last_key] = [current_adapter[last_key], stripped]  # type: ignore
                current_adapter[last_key].append(stripped)  # type: ignore
                continue

            if ":" not in line:
                continue

            parts: List[str] = stripped.split(":", 1)
            key = sanitize_key(parts[0])
            value = parts[1].strip()
            current_adapter[key] = value
            last_key = key

    return result


def main():
    results: List[Dict[str, str | List[str]]] = []

    for entry in sorted(Path(".").glob("*.txt")):
        raw = Path(entry.name).read_text(encoding="utf-16")
        results.append(parse_ipconfig(entry.name, raw))

    print(json.dumps(results, indent=2, ensure_ascii=False))

    with open("output.json", "w", encoding="utf-16") as out:
        json.dump(results, out, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()