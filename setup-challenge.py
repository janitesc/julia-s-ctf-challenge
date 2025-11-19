import sys
import os
import json
import subprocess
from pathlib import Path
import re
import secrets

def main():
    here = Path(__file__).resolve().parent
    os.chdir(here)
    raw_flag = os.environ.get("FLAG")

    # Try to get FLAG from environment; fall back to a dummy during build
    if not raw_flag:
        print("WARNING: FLAG environment variable not set; using DUMMY suffix for build")
        flag_rand = secrets.token_hex(4)
    else:
        m = re.search(r"\{([^}]*)\}$", raw_flag)
        if not m:
            print("WARNING: FLAG isn't wrapped by curly braces; using entire FLAG as suffix")
            flag_rand = raw_flag
        else:
            flag_rand = m.group(1)

    # Construct the actual flag players must submit
    flag = f"picoCTF{{omg_proper_memdump_analysis_{flag_rand}}}"
    print(flag)
    env = os.environ.copy()
    env["FLAG"] = flag
    # generat ememdump
    try:
        subprocess.run(["/challenge/start.sh"], check=True, env=env)
        print("start.sh executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing start.sh: {e}")
        sys.exit(1)

    # Ensure memdump.bin (or memdump.*) exists 
    memdump = None
    for name in os.listdir("."):
        if name.startswith("memdump."):
            memdump = name
            break

    if memdump is None:
        print("No memdump.* found! Aborting.")
        sys.exit(1)

    if memdump != "memdump.bin":
        os.rename(memdump, "memdump.bin")

    # Create metadata.json with the REAL flag
    metadata = {"flag": flag}
    with open("metadata.json", "w") as f:
        json.dump(metadata, f)

    # Pack memdump.bin into artifacts.tar.gz
    subprocess.run(
        ["tar", "czf", "artifacts.tar.gz", "memdump.bin"],
        check=True,
    )

    print("Created metadata.json and artifacts.tar.gz in /challenge.")


if __name__ == "__main__":
    main()
