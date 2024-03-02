# filename: wifi_config.py

import re

# Define the path of the input and output files
input_file = "/RelicConf/wificonf.txt"
output_file = "/etc/wpa_supplicant/wpa_supplicant.conf"

# Define the pattern to match the SSID and password
pattern = r"(?P<ssid>\S+)\s+(?P<pwd>\S+)"

# Read the input file and extract the WiFi credentials
wifi_credentials = []
with open(input_file, "r") as f:
    for line in f:
        match = re.search(pattern, line)
        if match:
            ssid = match.group("ssid")
            pwd = match.group("pwd")
            wifi_credentials.append((ssid, pwd))

if not wifi_credentials:
    print("No WiFi credentials found in the input file.")
    exit(1)

# Read the original wpa_supplicant.conf file
with open(output_file, "r") as f:
    original_content = f.read()

# Find the index of the first network block
index = original_content.find("network={")

if index == -1:
    print("No network block found in the wpa_supplicant.conf file.")
    exit(1)

# Keep the original content up to the first network block
new_content = original_content[:index]

# Add the new network blocks
for ssid, pwd in wifi_credentials:
    network_block = f"""
network={{
    ssid="{ssid}"
    psk="{pwd}"
    key_mgmt=WPA-PSK
}}
"""
    new_content += network_block

# Write the new content back to the wpa_supplicant.conf file
with open(output_file, "w") as f:
    f.write(new_content)

print("The wpa_supplicant.conf file has been updated successfully.")
