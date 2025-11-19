import sys
import os
import subprocess
import re
import json
import secrets


def main():
    #spoofing an "evil" actor that is deleting a flag
    flag = os.environ.get("FLAG")
    flag_bytes = flag.encode("utf-8")
    with open("flag.txt", "w") as f:
        f.write(flag)
    with open("flag.txt", "rb") as f:
        _ = f.read()
    os.remove ("flag.txt")
    #make a fake process memory
    dump = bytearray(secrets.token_bytes(4096))

    path_info = b"deleted file: /home/ctf/flag.txt\n"
    marker = b"[FLAG_CONTENTS_START]\n"
    header = path_info + marker
    header_len = len(header)
    if header_len + len(flag_bytes) + 1 > 4096:
        raise RuntimeError("size too small for header + flag")

    dump[0:header_len] = header

    base_offset = max(header_len + 16, 1024)
    max_offset = 4096 - (len(flag_bytes) + 1)
    if base_offset > max_offset:
        raise RuntimeError("not enough room for flag")

    leak_offset = secrets.randbelow(max_offset - base_offset + 1) + base_offset

    dump[leak_offset:leak_offset + len(flag_bytes)] = flag_bytes
    dump[leak_offset + len(flag_bytes)] = 0x00

    with open("memdump.raw", "wb") as f:
        f.write(dump)

    print("malicious.py: wrote memdump.raw with new flag.")

#I want to include secret evil process amongs a bunch of normal processes for part 2
#ie I want to keep the PID element but I need to get the dynamic flag thing to work first

    # if os.path.exists("flag.txt"):
    #     with open("flag.txt", "rb") as f:
    #         data = f.read()

    #     pid = os.getpid()
        
    #     print("Loaded flag.txt into memory.")
    #     print("PID:", pid)
    #     print("data", data)
    #     #waiting here 
    #     print("deleting file mwahaha")

    #     core_prefix = "memdump"
    #     try: 
    #         subprocess.run(
    #             ["gcore", "-o", core_prefix, str(pid)],
    #             check = True,
    #         )
    #         print(f"Memory dump written to {core_prefix}.{pid}")
    #     except FileNotFoundError: 
    #         print("there was no file of that name")
    #     except subprocess.CalledProcessError:
    #         print("subprocess error")


    #     os.remove("flag.txt")

    #     print("removed this file!!: ", "flag.txt")
    # else:
    #     print("file to remove does not exist")
    
    



if __name__ == "__main__":
    main()