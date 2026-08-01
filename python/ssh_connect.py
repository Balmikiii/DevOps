#!/usr/bin/env python3

import os
import subprocess

CONFIG = os.path.expanduser("~/.ssh/config")


def get_hosts():
    hosts = []

    with open(CONFIG, "r") as f:
        for line in f:
            line = line.strip()

            if line.lower().startswith("host "):
                for host in line.split()[1:]:
                    if "*" not in host and "?" not in host:
                        hosts.append(host)

    return hosts


def main():
    if not os.path.exists(CONFIG):
        print(f"SSH config not found: {CONFIG}")
        return

    hosts = get_hosts()

    if not hosts:
        print("No SSH hosts found.")
        return

    print("\n========== SSH MENU ==========\n")

    for i, host in enumerate(hosts, start=1):
        print(f"{i}. {host}")
    print("0. Exit")

    while True:
        try:
            choice = int(input("\nSelect server: "))
            if choice == 0:
                print("Exiting...")
                return

            if 1 <= choice <= len(hosts):
                break

            print("Invalid selection.")

        except ValueError:
            print("Enter a valid number.")

    selected = hosts[choice - 1]

    print(f"\nConnecting to {selected}...\n")

    subprocess.run(["ssh", selected])


if __name__ == "__main__":
    main()

