import re
from Config import ADAPTER_KEYS, LIST_FIELDS

_PARENS = re.compile(r"\(.*?\)")


def _resolve_key(raw: str) -> str | None:
    cleaned = " ".join(raw.replace(".", "").lower().strip().split())
    return ADAPTER_KEYS.get(cleaned)


def _clean_value(value: str, key: str) -> str:
    value = value.strip()
    if key.startswith(("ipv4", "ipv6", "subnet", "gateway", "physical")):
        value = _PARENS.sub("", value).strip()
    return value


def _blank_adapter(name: str) -> dict:
    adapter = {key: ([] if key in LIST_FIELDS else "") for key in (
        "adapter_name", "description", "physical_address",
        "dhcp_enabled", "autoconfiguration_enabled",
        "ipv4_address", "ipv6_address", "ipv6_temporary", "ipv6_link_local",
        "subnet_mask", "default_gateway",
        "dhcp_server", "lease_obtained", "lease_expires",
        "dns_servers", "dns_suffix",
        "dhcpv6_iaid", "dhcpv6_duid",
        "media_state", "netbios_over_tcpip",
    )}
    adapter["adapter_name"] = name
    return adapter


def parse_file(text: str) -> list[dict]:
    adapters: list[dict] = []
    current: dict | None = None
    active_key: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line or "windows ip configuration" in line.lower():
            continue

        is_header = (
            not raw_line.startswith((" ", "\t"))
            and line.endswith(":")
            and "adapter" in line.lower()
        )

        if is_header:
            current = _blank_adapter(line[:-1].strip())
            adapters.append(current)
            active_key = None
            continue

        if current is None:
            continue

        if ":" not in line:
            if active_key and active_key in LIST_FIELDS:
                val = _clean_value(line, active_key)
                if val:
                    current[active_key].append(val)
            continue

        raw_key, _, raw_val = line.partition(":")
        key = _resolve_key(raw_key)
        if key is None:
            active_key = None
            continue

        val = _clean_value(raw_val, key)
        active_key = key

        if key in LIST_FIELDS:
            if val:
                current[key].append(val)
        else:
            current[key] = val

    return adapters