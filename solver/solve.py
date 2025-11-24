import sys
import re

#double checking submission concept works
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


def extract_flag(dump_path: str) -> str:
    with open(dump_path, "rb") as f:
        data = f.read()
    #finds suspicious process from download folder
    line_start = data.find(b"user/Downloads/")
    if line_start == -1:
        raise RuntimeError("couldn't find PID tag")
    
    line_end = data.find(b"\n", line_start)
    if line_end == -1:
        line_end = len(data)
    line_bytes = data[line_start:line_end]
    line_text = line_bytes.decode("ascii", errors="ignore")
    m = re.search(r"user/Downloads/flag\.txt\s+(\d+)", line_text)
    if not m:
        raise RuntimeError("couldn't parse PID from suspicious process line")
    suspicious_pid = int(m.group(1))

    #then greps for that pid
    pid_tag = f"[PID={suspicious_pid}] ".encode("ascii")
    positions = []
    pos = 0
    while True:
        idx = data.find(pid_tag, pos)
        if idx == -1: 
            break
        positions.append(idx)
        pos = idx+1
    if not positions:
        raise RuntimeError("couldn't find encrypted flag tag")
    tag_start = positions[-1]
    if tag_start == -1:
        raise RuntimeError("couldn't find encrypted flag tag for that PID")

    
    enc_start = tag_start + len(pid_tag)
    enc_end = data.find(b"\x00", enc_start)
    if enc_end == -1:
        raise RuntimeError("couldn't find null terminator after encrypted flag")

    enc_flag = data[enc_start:enc_end]

    #then decodes it
    dec_bytes = bytes(atbash(b) for b in enc_flag)
    flag = dec_bytes.decode("utf-8", errors="ignore").strip()

    return flag



def main():


    dump_path = "memdump.bin"
    flag = extract_flag(dump_path)
    print(flag)
    sys.exit(0)

if __name__ == "__main__":
    main()