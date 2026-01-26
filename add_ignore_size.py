
import os

service_path = "/etc/systemd/system/charterstone.service"
temp_path = "charterstone.service.tmp_size_flag"

with open(service_path, "r") as f:
    content = f.read()

# Exact block to find (based on previous state)
old_block = """ExecStartPre=/usr/bin/rclone mount charterstone: /home/aaronshirley751/charterstone-mount \\
    --vfs-cache-mode writes \\
    --no-checksum \\
    --no-modtime \\
    --daemon \\
    --allow-non-empty"""

# New block with --ignore-size inserted
new_block = """ExecStartPre=/usr/bin/rclone mount charterstone: /home/aaronshirley751/charterstone-mount \\
    --vfs-cache-mode writes \\
    --no-checksum \\
    --no-modtime \\
    --ignore-size \\
    --daemon \\
    --allow-non-empty"""

if old_block in content:
    new_content = content.replace(old_block, new_block)
    with open(temp_path, "w") as f:
        f.write(new_content)
    print("Replacement ready.")
else:
    print("Could not find the exact block to replace.")
    print("Content snippet trying to match against:")
    start_index = content.find("ExecStartPre=/usr/bin/rclone")
    if start_index != -1:
        print(content[start_index:start_index+300])
    else:
        print("Could not find ExecStartPre=/usr/bin/rclone line.")
