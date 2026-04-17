import json
from pathlib import Path

def sanitize_key(raw_key):
    clean = raw_key.replace(".", "").strip().lower()
    clean = clean.replace("-", "_").replace(" ", "_")
    return clean

def parse_network_config(file_path):
    try:
        content = file_path.read_text(encoding="utf-8").splitlines()
    except:
        content = file_path.read_text(encoding="latin-1").splitlines()

    file_report = {"file_name": file_path.name, "adapters": []}
    current_adapter = None
    last_key = None

    for line in content:
        stripped = line.strip()

        if not stripped:
            continue

        if not line.startswith(" ") and stripped.endswith(":"):
            if current_adapter is not None:
                file_report["adapters"].append(current_adapter)

            current_adapter = {"adapter_name": stripped[:-1]}
            last_key = None
            continue

        if current_adapter is not None:
            if ":" in stripped:
                parts = stripped.split(":", 1)
                key = sanitize_key(parts[0])
                value = parts[1].strip()

                current_adapter[key] = value
                last_key = key
            
            elif last_key is not None and line.startswith(" "):
                prev_value = current_adapter[last_key]
                
                if isinstance(prev_value, str):
                    current_adapter[last_key] = [prev_value, stripped]
                else:
                    current_adapter[last_key].append(stripped)

    if current_adapter is not None:
        file_report["adapters"].append(current_adapter)

    return file_report

def main():
    final_output = []

    for file_name in Path(".").glob("*.txt"):
        data = parse_network_config(file_name)
        final_output.append(data)

    with open("adapters_config.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()