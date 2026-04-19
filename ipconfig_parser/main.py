import json
from pathlib import Path
from typing import List, Dict, Any, Optional

class IpConfigParser:
    MULTI_VALUE_KEYS = {"dns_servers", "default_gateway"}
    JSON_KEYS = {
        "description", "physical_address", "dhcp_enabled", 
        "ipv4_address", "subnet_mask", "default_gateway", "dns_servers"
    }
    
    LABEL_MAPPING = {
        "Description": "description",
        "Physical Address": "physical_address",
        "DHCP Enabled": "dhcp_enabled",
        "IPv4 Address": "ipv4_address",
        "Autoconfiguration IPv4 Address": "ipv4_address",
        "Subnet Mask": "subnet_mask",
        "Default Gateway": "default_gateway",
        "DNS Servers": "dns_servers",
    }

    def _init_adapter(self, name: str) -> Dict[str, Any]:
        adapter = {"adapter_name": name}
        for key in self.JSON_KEYS:
            adapter[key] = [] if key in self.MULTI_VALUE_KEYS else ""
        return adapter

    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        try:
            content = file_path.read_text(encoding="utf-16")
        except UnicodeDecodeError:
            content = file_path.read_text(encoding="utf-8", errors="replace")

        parsed_data = {"file_name": file_path.name, "adapters": []}
        current_adapter: Optional[Dict[str, Any]] = None
        last_key: Optional[str] = None

        for line in content.splitlines():
            clean_line = line.strip()
            if not clean_line:
                continue

            if not line.startswith((" ", "\t")) and clean_line.endswith(":"):
                if current_adapter:
                    parsed_data["adapters"].append(current_adapter)
                current_adapter = self._init_adapter(clean_line[:-1])
                last_key = None
                continue

            if current_adapter is not None:
                if ":" in line:
                    label_part, value_part = line.split(":", 1)
                    label = label_part.replace(".", "").strip()
                    found_key = self.LABEL_MAPPING.get(label)

                    if found_key:
                        value = value_part.split("(")[0].strip()
                        if found_key in self.MULTI_VALUE_KEYS:
                            if value:
                                current_adapter[found_key].append(value)
                        else:
                            current_adapter[found_key] = value
                        last_key = found_key
                
                elif last_key in self.MULTI_VALUE_KEYS and line.startswith("      "):
                    if clean_line:
                        current_adapter[last_key].append(clean_line)

        if current_adapter:
            parsed_data["adapters"].append(current_adapter)

        return parsed_data

def main():
    parser = IpConfigParser()
    results = []
    excluded_files = {"requirements.txt", "output.json"}
    
    for path in sorted(Path(".").glob("*.txt")):
        if path.name not in excluded_files:
            results.append(parser.parse_file(path))

    output_json = Path("output.json")
    json_output = json.dumps(results, indent=2, ensure_ascii=False)
    
    print(json_output)
    output_json.write_text(json_output, encoding="utf-8")

if __name__ == "__main__":
    main()