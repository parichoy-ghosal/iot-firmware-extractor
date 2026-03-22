import pexpect
import re
import time
import sys

PORT = '/dev/ttyUSB0'
BAUD = 115200

START_ADDR = 0
END_ADDR = 2097152      # change to appropriate end address for full dump 
STEP = 256

OUTPUT_FILE = "firmware.bin"
LOG_FILE = "dump_log.txt"

line_regex = re.compile(r'^[0-9A-Fa-f]{8}:')

def extract_bytes(line):
    try:
        hex_part = line.split(':', 1)[1]
    except:
        return b''

    data = bytearray()

    for token in hex_part.strip().split():
        if len(token) == 2:
            try:
                data.append(int(token, 16))
            except:
                pass

    return bytes(data)


def read_output(child):
    """
    Read all available output without blocking forever
    """
    output = ""

    for _ in range(10):  # try multiple reads
        try:
            chunk = child.read_nonblocking(size=4096, timeout=0.3)
            output += chunk
        except:
            break

    return output


def main():
    print("[*] Starting dump...")

    child = pexpect.spawn(
        f'picocom -b {BAUD} --omap crlf {PORT}',
        encoding='utf-8',
        timeout=1
    )

    time.sleep(2)

    # Wake shell
    child.sendline('')
    time.sleep(1)

    with open(OUTPUT_FILE, "wb") as fw, open(LOG_FILE, "w") as log:
        addr = START_ADDR

        while addr < END_ADDR:
            cmd = f"flash_dump {addr} {STEP}"
            print(f"[>] {cmd}")

            child.sendline(cmd)

            time.sleep(0.4)

            output = read_output(child)

            log.write(output)
            log.flush()

            total = 0

            for line in output.split('\n'):
                if line_regex.match(line.strip()):
                    data = extract_bytes(line)
                    fw.write(data)
                    total += len(data)

            if total == 0:
                print(f"[!] Retry at {addr:08X}")
                time.sleep(1)
                continue

            print(f"[+] {addr:08X} → {total} bytes")

            addr += STEP

            # Progress indicator
            progress = (addr / END_ADDR) * 100
            print(f"[Progress] {progress:.2f}%")

            time.sleep(0.05)

    child.close()

    print("[✓] Dump complete!")
    print(f"[✓] Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(0)
