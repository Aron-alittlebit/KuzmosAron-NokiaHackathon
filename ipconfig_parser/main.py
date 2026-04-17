import json
from pathlib import Path

def sanitize_key(raw_key: str) -> str:
    clean_name = raw_key.replace('.', '').strip().lower()
    clean_name = clean_name.replace('-', '_').replace(' ', '_')
    return clean_name

def parse_network_config(file_path: Path) -> dict:
    content = file_path.read_text(encoding="utf-16", errors="ignore").splitlines()

    file_report = {"file_name": file_path.name, "adapters": []}
    current_adapter = {"adapter_name": ""}
    last_processed_key = None

    for line in content:
        stripped_line = line.strip()
        
        if not stripped_line: 
            continue

        if not line.startswith((' ', '\t')) and stripped_line.endswith(':'):
            if len(current_adapter) > 1:
                file_report["adapters"].append(current_adapter)

            adapter_header = stripped_line[:-1].strip()
            current_adapter = {"adapter_name": adapter_header}
            last_processed_key = None
            continue

        if current_adapter is not None:
            if ':' in line:
                key_raw, value_raw = line.split(':', 1)
                formatted_key = sanitize_key(key_raw)
                formatted_value = value_raw.strip()
                
                current_adapter[formatted_key] = formatted_value
                last_processed_key = formatted_key
                
            elif last_processed_key:
                previous_value = current_adapter[last_processed_key]

                if isinstance(previous_value, str):
                    current_adapter[last_processed_key] = [previous_value, stripped_line]
                else:
                    current_adapter[last_processed_key].append(stripped_line)

    if len(current_adapter) > 1:
        file_report["adapters"].append(current_adapter)

    return file_report

def main():
    final_output = []

    for log_file in sorted(Path(".").glob("*.txt")):
        parsed_result = parse_network_config(log_file)
        final_output.append(parsed_result)

    json_payload = json.dumps(final_output, indent=2, ensure_ascii=False)
    
    Path("adapters_config.json").write_text(json_payload, encoding="utf-8")
    print(json_payload)

if __name__ == "__main__":
    main()