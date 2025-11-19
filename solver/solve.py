import sys

#double checking submission concept works


EXPECTED = "dummy_ctf_flag_yeehaw"

def extract_flag(dump_path: str) -> str:
    with open(dump_path, "rb") as f:
        data = f.read()
    start = data.find(b"picoCTF{")
    if start == -1:
        raise RuntimeError("couldn't find the flag prefix")
    end = data.find(b"}", start)

    if end == -1: 
        
        raise RuntimeError("couldn't find the flag ending brace")
    return data[start:end+1].decode("utf-8", errors="ignore")


def main():


    dump_path = "memdump.bin"
    flag = extract_flag(dump_path)
    print(flag)
    sys.exit(0)

if __name__ == "__main__":
    main()