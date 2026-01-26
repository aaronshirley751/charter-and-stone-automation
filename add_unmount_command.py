
import os

service_path = "/etc/systemd/system/charterstone.service"
temp_path = "charterstone.service.tmp_add_cmd"

new_line = "ExecStartPre=-/bin/fusermount -uz /home/aaronshirley751/charterstone-mount\n"
target_line = "ExecStartPre=/usr/bin/mkdir -p /home/aaronshirley751/charterstone-mount"

with open(service_path, "r") as f:
    lines = f.readlines()

new_lines = []
inserted = False
for line in lines:
    if target_line in line and not inserted:
        new_lines.append(new_line)
        inserted = True
    new_lines.append(line)

with open(temp_path, "w") as f:
    f.writelines(new_lines)

if inserted:
    print("Line inserted successfully.")
else:
    print("Target line not found.")
