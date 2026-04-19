from typing import Final

ENCODINGS: Final = (
    "utf-8-sig", "utf-16", "utf-16-le", "utf-16-be",
    "utf-8", "cp1250", "cp1252", "latin-1", "iso-8859-2",
)

ADAPTER_KEYS: Final = {
    "ipv4 address":                   "ipv4_address",
    "autoconfiguration ipv4 address": "ipv4_address",
    "ipv6 address":                   "ipv6_address",
    "temporary ipv6 address":         "ipv6_temporary",
    "link-local ipv6 address":        "ipv6_link_local",
    "subnet mask":                    "subnet_mask",
    "default gateway":                "default_gateway",
    "dhcp enabled":                   "dhcp_enabled",
    "dhcp server":                    "dhcp_server",
    "lease obtained":                 "lease_obtained",
    "lease expires":                  "lease_expires",
    "dns servers":                    "dns_servers",
    "connection-specific dns suffix": "dns_suffix",
    "description":                    "description",
    "physical address":               "physical_address",
    "dhcpv6 iaid":                    "dhcpv6_iaid",
    "dhcpv6 client duid":             "dhcpv6_duid",
    "media state":                    "media_state",
    "netbios over tcpip":             "netbios_over_tcpip",
    "autoconfiguration enabled":      "autoconfiguration_enabled",
}

OUTPUT_FIELDS: Final = [
    "adapter_name", "description", "physical_address",
    "dhcp_enabled", "ipv4_address", "subnet_mask",
    "default_gateway", "dns_servers",
]

LIST_FIELDS: Final = {"default_gateway", "dns_servers"}