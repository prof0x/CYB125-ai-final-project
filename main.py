"""
main.py
=======
CYB 125 Final Project — STARTER CODE
Windows Baseline Snapshot Generator

This file is the entry point. It builds an empty snapshot dictionary,
calls each collector function in helpers.py to fill it in, then
saves the result to a JSON file.

----------------------------------------------------------------------
HOW TO USE THIS FILE
----------------------------------------------------------------------

When you start, only Milestone 1 is active. The collector calls for
Milestones 2 through 8 are commented out below.

As you complete each milestone:
    1. Implement the matching function in helpers.py
    2. Come back to this file and UNCOMMENT the matching lines
    3. Run `python main.py` and verify the new section appears in the JSON
    4. Commit and push

Run the script from your Windows VM (not from a Codespace — Codespaces
are Linux containers and the Windows-only modules won't work there).

    > python main.py

The output JSON file goes in the current working directory and is
named like baseline_HOSTNAME_YYYYMMDDTHHMMSSZ.json
"""

import json
import time
import datetime
import socket
import sys

import helpers


def main():
    # Make sure we are running on Windows. winreg, wmic, and friends
    # don't exist on Linux or macOS.
    if sys.platform != "win32":
        print("ERROR: This script only works on Windows.")
        return

    print("Windows Baseline Snapshot Generator")
    print("-----------------------------------")

    # Build an empty snapshot dictionary with all 16 sections present
    snapshot = helpers.make_empty_snapshot()

    # Fill in the metadata section first so we know who/what/when even
    # if a later collector crashes
    snapshot["snapshot_metadata"] = helpers.get_snapshot_metadata(snapshot)

    print("Hostname: " + snapshot["snapshot_metadata"].get("hostname", "?"))
    print("User:     " + snapshot["snapshot_metadata"].get("generated_by_user", "?"))
    print("Elevated: " + str(snapshot["snapshot_metadata"].get("elevated", False)))
    if not snapshot["snapshot_metadata"].get("elevated", False):
        print("WARNING: Not running as Administrator.")
        print("         BitLocker status and some registry keys will be empty.")
    print("")

    # Time how long collection takes (recorded into metadata at the end)
    start_time = time.time()

    # ===== Milestone 1 =====
    # (Already done — get_snapshot_metadata above is your Milestone 1 work.)

    # ===== Milestone 2 =====
    print("Collecting system identity...")
    snapshot["system_identity"] = helpers.get_system_identity(snapshot)

    # ===== Milestone 3 =====
    print("Collecting password policy...")
    snapshot["password_policy"] = helpers.get_password_policy(snapshot)

    # ===== Milestone 4 =====
    # print("Collecting installed software...")
    # snapshot["installed_software"] = helpers.get_installed_software(snapshot)

    # ===== Milestone 5 =====
    # print("Collecting running processes...")
    # helpers.add_running_processes(snapshot)   # mutator — no assignment

    # ===== Milestone 6 =====
    # print("Collecting persistence locations...")
    # snapshot["persistence_locations"] = helpers.get_persistence_locations(snapshot)

    # ===== Milestone 7 =====
    # print("Collecting network configuration...")
    # snapshot["network_configuration"] = helpers.get_network_configuration(snapshot)
    # print("Collecting listening ports...")
    # helpers.add_listening_ports(snapshot)     # mutator — no assignment

    # ===== Milestone 8 =====
    # print("Collecting network shares...")
    # snapshot["network_shares"] = helpers.get_network_shares(snapshot)
    # print("Collecting installed hotfixes...")
    # snapshot["installed_hotfixes"] = helpers.get_installed_hotfixes(snapshot)
    # print("Collecting local user accounts...")
    # snapshot["local_user_accounts"] = helpers.get_local_user_accounts(snapshot)
    # print("Collecting hardware profile...")
    # snapshot["hardware_profile"] = helpers.get_hardware_profile(snapshot)
    # print("Collecting security posture...")
    # snapshot["security_posture"] = helpers.get_security_posture(snapshot)
    # print("Collecting performance snapshot...")
    # snapshot["performance_snapshot"] = helpers.get_performance_snapshot(snapshot)
    # print("Collecting scheduled tasks... (this can be slow)")
    # snapshot["scheduled_tasks"] = helpers.get_scheduled_tasks(snapshot)
    # print("Collecting auto-start services... (this is the slowest one)")
    # snapshot["auto_start_services"] = helpers.get_auto_start_services(snapshot)

    # Record how long the whole collection took
    duration = time.time() - start_time
    snapshot["snapshot_metadata"]["collection_duration_seconds"] = round(duration, 2)

    # Build the output filename: baseline_HOSTNAME_TIMESTAMP.json
    hostname = socket.gethostname()
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    output_filename = "baseline_" + hostname + "_" + timestamp + ".json"

    # Save the snapshot to a JSON file. The default=str argument is a
    # safety net — if any field somehow holds a value that JSON doesn't
    # natively understand (like a datetime object), it'll be converted
    # to its string representation instead of crashing the dump.
    try:
        with open(output_filename, "w") as f:
            json.dump(snapshot, f, indent=2, default=str)
        print("")
        print("Done! Saved to " + output_filename)
        print("Took " + str(round(duration, 2)) + " seconds.")

        warnings = snapshot["snapshot_metadata"].get("collection_warnings", [])
        print("Warnings: " + str(len(warnings)))
        for w in warnings:
            print("  - " + w)
    except Exception as e:
        print("ERROR writing JSON file: " + str(e))


if __name__ == "__main__":
    main()
