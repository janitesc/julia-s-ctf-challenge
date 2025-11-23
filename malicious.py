import sys
import os
import subprocess
import re
import json
import secrets


#encoding it with atbash because it's a very easy cipher to solve + I feel the 
#challenge is too easy otherwise
def atbash(c: int) -> int:
    ch = c

    # uppercase
    if ord('A') <= ch <= ord('Z'):
        a = ord('A')
        z = ord('Z')
        x = z - (ch - a)
        return x

    # lowercase
    if ord('a') <= ch <= ord('z'):
        a = ord('a')
        z = ord('z')
        x = z - (ch - a)
        return x

    # numbers
    if ord('0') <= ch <= ord('9'):
        a = ord('0')
        z = ord('9')
        x = z - (ch - a)         
        return x
    return ch



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



    #fake process table
    pids = [secrets.randbelow(5000) + 1000 for _ in range(6)]
    suspicious_pid = secrets.choice(pids)
    benign_dirs = ["Desktop", "Documents", "Pictures", "Music", "Work"]

    lines = []
    lines.append(b"USER       PID COMMAND\n")
    #change users for fun
    for pid in pids:
        if pid == suspicious_pid:
            user_path = "user/Downloads/flag.txt"
        else:
            # Benign ones: different dirs doing something boring
            dir_name = secrets.choice(benign_dirs)
            user_path = f"user/{dir_name}/"


        line = f"{user_path:<26} {pid:<5d} \n"
        lines.append(line.encode("ascii"))
    enc_config = (
        "ENCRYPTION_SCHEME: I love Atbash! My favorite Cipher!!\n"
     ).encode("ascii")
    lines.append(enc_config)

    proc_table = b"".join(lines)



    header = proc_table
    header_len = len(header)
    if header_len >= 4096:
        raise RuntimeError("Header too large for dump size")

    dump[0:header_len] = header
    enc_flag = bytes(atbash(c) for c in flag_bytes)

    pid_tag = f"[PID={suspicious_pid}] ".encode("ascii")

    base_offset = max(header_len + 16, 1024)
    max_offset = 4096 - (len(enc_flag) + 1)
    if base_offset > max_offset:
        raise RuntimeError("not enough room for flag")

    leak_offset = secrets.randbelow(max_offset - base_offset + 1) + base_offset

    dump[leak_offset:leak_offset + len(pid_tag)] = pid_tag
    flag_start = leak_offset + len(pid_tag)
    dump[flag_start:flag_start + len(flag_bytes)] = enc_flag
    dump[flag_start + len(enc_flag)] = 0x00   

    with open("memdump.raw", "wb") as f:
        f.write(dump)

    print("malicious.py: wrote memdump.raw with new flag.")
    



if __name__ == "__main__":
    main()