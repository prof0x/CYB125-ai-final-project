"""
helpers.py
==========
CYB 125 Final Project — STARTER CODE
Windows Baseline Snapshot Generator

This file gives you everything you need to start. It contains:

    1. make_empty_snapshot()   — builds the empty snapshot dictionary
    2. run_command()           — runs a Windows command, returns its output
    3. get_registry_value()    — reads one value from the Windows Registry
    4. add_warning()           — mutator function that appends to the snapshot
    5. get_snapshot_metadata() — fully implemented EXAMPLE collector (Milestone 1)
    6. Empty stubs for the 15 collector functions you will write across
       Milestones 2 through 8

----------------------------------------------------------------------
HOW TO USE THIS FILE
----------------------------------------------------------------------

* Read sections 1-5 carefully BEFORE you start Milestone 2.
* For each milestone, find the matching `# TODO Milestone N` block
  below and replace it with your implementation.
* Each TODO block tells you (a) which fields to collect, (b) where
  the data comes from, (c) what one populated entry looks like, and
  (d) where to look in the textbook if you forget how something works.
* The pattern in `get_snapshot_metadata()` is the same pattern every
  other collector follows. When in doubt, copy that pattern.
"""

import subprocess
import winreg
import socket
import getpass
import platform
import os
import json
import csv
import io
import datetime
import ctypes


# ===================================================================
# 1. The snapshot dictionary
# ===================================================================
# This function returns a fresh, empty snapshot dict with all 16
# sections pre-created. Some sections start as {} (a dict) because
# they will hold a single record. Others start as [] (a list)
# because they will hold many records (e.g. one entry per process).
#
# Compare this shape to example_baseline.json — they match exactly,
# except every value here is empty.

def make_empty_snapshot():
    snapshot = {
        "snapshot_metadata": {},
        "system_identity": {},
        "hardware_profile": {},
        "network_configuration": {},
        "listening_ports": [],
        "local_user_accounts": {},
        "password_policy": {},
        "auto_start_services": [],
        "running_processes": [],
        "installed_software": [],
        "installed_hotfixes": [],
        "persistence_locations": {},
        "scheduled_tasks": [],
        "security_posture": {},
        "performance_snapshot": {},
        "network_shares": [],
    }
    return snapshot


# ===================================================================
# 2. Helper to run a Windows command
# ===================================================================
# `command_list` is a list of strings, like ["ipconfig", "/all"]
# Returns the text the command printed (its stdout), or "" if
# something broke.
#
# IMPORTANT: every Windows command you call from Python in this
# project goes through this helper. You do NOT need to call
# subprocess.run yourself anywhere else.

def run_command(command_list):
    try:
        result = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except Exception:
        return ""


# ===================================================================
# 3. Helper to read one value from the Windows Registry
# ===================================================================
# Returns the value, or None if the key/value isn't there.
# Example call:
#     get_registry_value(
#         winreg.HKEY_LOCAL_MACHINE,
#         r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
#         "ProductName"
#     )
#
# Notice the `r` before the string — this is a "raw string" so that
# the backslashes are treated as literal characters instead of escape
# sequences. Always use raw strings for registry paths.

def get_registry_value(hive, subkey, value_name):
    try:
        key = winreg.OpenKey(hive, subkey)
        value, value_type = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)
        return value
    except Exception:
        return None


# ===================================================================
# 4. The mutator function — adds a warning to the snapshot
# ===================================================================
# This is one of the two function styles the assignment requires.
# Notice that it returns None and modifies the snapshot dict directly.
# That's why we don't write `snapshot = add_warning(snapshot, ...)` —
# we just call `add_warning(snapshot, ...)` on its own line.
#
# YOU WILL CALL THIS FUNCTION from inside every except block in the
# 15 collectors below. The pattern looks like:
#     except Exception as e:
#         add_warning(snapshot, "<section_name> failed: " + str(e))

def add_warning(snapshot, message):
    if "collection_warnings" not in snapshot["snapshot_metadata"]:
        snapshot["snapshot_metadata"]["collection_warnings"] = []
    snapshot["snapshot_metadata"]["collection_warnings"].append(message)


# ===================================================================
# 5. EXAMPLE COLLECTOR — Snapshot Metadata (Milestone 1, done for you)
# ===================================================================
# This is the WORKED EXAMPLE for the project. Read every line.
# It demonstrates the pattern every other collector must follow:
#
#     def get_<thing>(snapshot):
#         info = {}    # or []  if returning a list
#         try:
#             ... gather data ...
#             info["some_key"] = some_value
#         except Exception as e:
#             add_warning(snapshot, "<thing> failed: " + str(e))
#         return info
#
# Why does it take `snapshot` as an argument if it returns a dict?
# So that it can call add_warning() if something goes wrong —
# add_warning needs the snapshot to know where to append the message.

def get_snapshot_metadata(snapshot):
    info = {}
    try:
        # Check whether we are running as Administrator.
        # ctypes.windll is a Windows-only Python feature that lets us
        # call into Windows DLLs. shell32.IsUserAnAdmin() returns 1
        # if the current process has Administrator rights, 0 otherwise.
        is_admin = False
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            is_admin = False

        info["schema_version"] = "1.0"
        info["timestamp_utc"] = datetime.datetime.utcnow().isoformat() + "Z"
        info["hostname"] = socket.gethostname()
        info["generated_by_user"] = getpass.getuser()
        info["elevated"] = is_admin
        info["script_version"] = "1.0.0"
        info["python_version"] = platform.python_version()
        info["collection_duration_seconds"] = None  # filled in by main.py at the end
        info["collection_warnings"] = []
    except Exception as e:
        # Safety net — if any of the Python-stdlib calls above somehow fail,
        # we still want the dict to exist with at least a warning in it.
        info["collection_warnings"] = ["snapshot_metadata partial: " + str(e)]
    return info


# ===================================================================
# 6. STUB COLLECTORS — fill these in across Milestones 2 through 8
# ===================================================================
# Each stub below has a detailed comment block that tells you:
#   - which fields to collect (and the type each field should be)
#   - where the data comes from
#   - what one populated entry would look like
#   - which textbook chapter to review if you're stuck
#
# The stubs themselves are placeholders that return empty results.
# Replace the body of each function with your real implementation.


# -------------------------------------------------------------------
# Milestone 2 — System Identity
# -------------------------------------------------------------------
# Read 5 values from the registry under:
#   HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion
#
# Fields to populate in `info`:
#   - "os_name"            (string)  from registry value: ProductName
#   - "os_build"           (string)  from registry value: CurrentBuild
#   - "os_edition"         (string)  from registry value: EditionID
#   - "registered_owner"   (string)  from registry value: RegisteredOwner
#   - "install_date_utc"   (string)  from registry value: InstallDate
#         IMPORTANT: InstallDate is a Unix timestamp (an integer like
#         1755139862). You need to convert it to a readable date string.
#         Use: datetime.datetime.utcfromtimestamp(install_epoch).isoformat() + "Z"
#         If install_epoch is None, leave install_date_utc as None.
#
# Example of what `info` should look like when you finish:
#   {
#     "os_name": "Windows 11 Enterprise",
#     "os_build": "22631",
#     "os_edition": "Enterprise",
#     "registered_owner": "student01",
#     "install_date_utc": "2025-08-14T03:11:02Z"
#   }
#
# Refresher: ATBS Ch. 4 (functions) and Ch. 5 (try/except).
# AI prompt: see Milestone 2 in the project spec.

def get_system_identity(snapshot):
    info = {}
    try:
        # Read the OS product name from the registry and store it as a string.
        info["os_name"] = get_registry_value(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
            "ProductName"
        )
        # Read the build number and store it as a string.
        info["os_build"] = get_registry_value(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
            "CurrentBuild"
        )
        # Read the Windows edition identifier and store it as a string.
        info["os_edition"] = get_registry_value(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
            "EditionID"
        )
        # Read the registered owner name and store it as a string.
        info["registered_owner"] = get_registry_value(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
            "RegisteredOwner"
        )
        # Read the raw install timestamp and convert it to an ISO UTC string.
        install_epoch = get_registry_value(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
            "InstallDate"
        )
        if install_epoch is None:
            info["install_date_utc"] = None
        else:
            # Use utcfromtimestamp() so the date is stable and not local-time dependent.
            info["install_date_utc"] = datetime.datetime.utcfromtimestamp(
                int(install_epoch)
            ).isoformat() + "Z"
    except Exception as e:
        add_warning(snapshot, "system_identity failed: " + str(e))
    return info


# -------------------------------------------------------------------
# Milestone 3 — Password Policy
# -------------------------------------------------------------------
# Run `net accounts` and parse each "Label: value" line.
#
# Fields to populate in `info` (all integers, or None if "Never"):
#   - "minimum_password_length"             — from "Minimum password length"
#   - "minimum_password_age_days"           — from "Minimum password age (days)"
#   - "maximum_password_age_days"           — from "Maximum password age (days)"
#   - "password_history_length"             — from "Length of password history maintained"
#   - "lockout_threshold"                   — from "Lockout threshold"
#   - "lockout_duration_minutes"            — from "Lockout duration (minutes)"
#   - "lockout_observation_window_minutes"  — from "Lockout observation window (minutes)"
#
# Tips:
#   - Run `net accounts` in your Windows terminal first to see the format.
#   - Use line.split(":", 1) to split on the FIRST colon only.
#   - Use .strip() to remove whitespace from both ends of each piece.
#   - Some values say "Never" instead of a number — store None for those.
#   - Wrap your int() conversion in try/except so a "Never" value
#     doesn't crash the whole function.
#
# Example of what `info` should look like when you finish:
#   {
#     "minimum_password_length": 0,
#     "minimum_password_age_days": 0,
#     "maximum_password_age_days": 42,
#     "password_history_length": 0,
#     "lockout_threshold": 0,
#     "lockout_duration_minutes": 30,
#     "lockout_observation_window_minutes": 30
#   }
#
# Refresher: ATBS Ch. 6 (strings) and Ch. 19 (running programs).
# AI prompt: see Milestone 3 in the project spec.

def get_password_policy(snapshot):
    info = {}
    try:
        # Run `net accounts` to get the password policy output as a string.
        output = run_command(["net", "accounts"])
        
        # Walk through each line of output and parse "Label: value" pairs.
        for line in output.split("\n"):
            line = line.strip()
            
            # Skip empty lines — they don't contain policy data.
            if not line:
                continue
            
            # Split on the FIRST colon only (use split(":", 1)) because some
            # labels or values might contain colons. This gives us [label, value].
            if ":" not in line:
                continue
            
            label, _, value = line.partition(":")
            # Use partition() instead of split(":", 1) because it returns (before, sep, after),
            # which is slightly cleaner for this use case. Both approaches work.
            
            label = label.strip()
            value = value.strip()
            
            # Helper function to convert a value to int or None if it says "Never".
            # This is defined inline so we can reuse it for all 7 fields.
            def parse_int_or_never(val):
                if val.lower() == "never":
                    return None
                try:
                    return int(val)
                except ValueError:
                    return None
            
            # Map each label to its field name in the info dict, then parse and store.
            if label == "Minimum password length":
                info["minimum_password_length"] = parse_int_or_never(value)
            elif label == "Minimum password age (days)":
                info["minimum_password_age_days"] = parse_int_or_never(value)
            elif label == "Maximum password age (days)":
                info["maximum_password_age_days"] = parse_int_or_never(value)
            elif label == "Length of password history maintained":
                info["password_history_length"] = parse_int_or_never(value)
            elif label == "Lockout threshold":
                info["lockout_threshold"] = parse_int_or_never(value)
            elif label == "Lockout duration (minutes)":
                info["lockout_duration_minutes"] = parse_int_or_never(value)
            elif label == "Lockout observation window (minutes)":
                info["lockout_observation_window_minutes"] = parse_int_or_never(value)
    except Exception as e:
        add_warning(snapshot, "password_policy failed: " + str(e))
    return info


# -------------------------------------------------------------------
# Milestone 4 — Installed Software
# -------------------------------------------------------------------
# Walk every subkey under the Uninstall registry hive and append a
# dict for each entry that has a DisplayName.
#
# Registry path to walk:
#   HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall
#
# For each subkey, read these 4 registry values:
#   - DisplayName    (string) — if missing, SKIP this subkey entirely
#   - DisplayVersion (string)
#   - Publisher      (string)
#   - InstallDate    (string in YYYYMMDD format, e.g. "20250902")
#         Convert to ISO date "YYYY-MM-DD". If InstallDate is missing
#         (some MSI installers don't write it), leave it as None.
#
# Each entry you append to `software` should look like:
#   {
#     "display_name":    "Microsoft Visual Studio Code",
#     "display_version": "1.89.1",
#     "publisher":       "Microsoft Corporation",
#     "install_date":    "2025-09-02"
#   }
#
# How to walk the subkeys:
#   - Use winreg.OpenKey(hive, base_key) to open the parent key.
#   - Use winreg.EnumKey(key, i) in a loop, incrementing i, to get
#     each subkey name. EnumKey raises OSError when there are no
#     more subkeys — that's how you know to stop.
#   - For each subkey name, build the full path:
#         full_path = base_key + "\\" + sub_name
#     and pass that path to get_registry_value() to read the values.
#
# Refresher: ATBS Ch. 4 (lists), Ch. 7 (nested data structures).
# AI prompt: see Milestone 4 in the project spec.

def get_installed_software(snapshot):
    software = []
    try:
        # Open the Uninstall registry hive — this is where all registered programs live.
        # winreg.HKEY_LOCAL_MACHINE is the HKLM part of the path.
        hive = winreg.HKEY_LOCAL_MACHINE
        base_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        key = winreg.OpenKey(hive, base_path)
        
        # Walk through every subkey (each represents one installed program or entry).
        # We use a manual counter loop because winreg.EnumKey raises OSError when done,
        # not a Python StopIteration like a normal iterator.
        i = 0
        while True:
            try:
                # Get the name of the i-th subkey.
                subkey_name = winreg.EnumKey(key, i)
                
                # Build the full registry path to this subkey so we can read its values.
                full_subkey_path = base_path + "\\" + subkey_name
                
                # Read the DisplayName — this is the program's user-friendly name.
                # If there's no DisplayName, we skip this entry because it's not a real program.
                display_name = get_registry_value(hive, full_subkey_path, "DisplayName")
                if display_name is None:
                    i += 1
                    continue
                
                # Read the DisplayVersion — this is the version string like "1.0.0".
                display_version = get_registry_value(
                    hive,
                    full_subkey_path,
                    "DisplayVersion"
                )
                
                # Read the Publisher — the company that made the software.
                publisher = get_registry_value(hive, full_subkey_path, "Publisher")
                
                # Read the InstallDate — a string in YYYYMMDD format like "20250902".
                install_date_raw = get_registry_value(
                    hive,
                    full_subkey_path,
                    "InstallDate"
                )
                
                # Convert YYYYMMDD to ISO format (YYYY-MM-DD), or store None if missing.
                # We can slice the string directly: positions 0-3 are the year,
                # 4-5 are the month, 6-7 are the day. (Alternative: use datetime.strptime()
                # if you prefer, but string slicing is faster and doesn't need error handling.)
                if install_date_raw is None or len(install_date_raw) < 8:
                    install_date = None
                else:
                    install_date = (
                        install_date_raw[0:4] + "-" +
                        install_date_raw[4:6] + "-" +
                        install_date_raw[6:8]
                    )
                
                # Build the entry dict with all 4 fields and append it to the list.
                entry = {
                    "display_name": display_name,
                    "display_version": display_version,
                    "publisher": publisher,
                    "install_date": install_date
                }
                software.append(entry)
                
                # Move to the next subkey.
                i += 1
            except OSError:
                # No more subkeys — exit the loop.
                break
        
        # Close the registry key to free the resource.
        winreg.CloseKey(key)
    except Exception as e:
        add_warning(snapshot, "installed_software failed: " + str(e))
    return software


# -------------------------------------------------------------------
# Milestone 5 — Running Processes (MUTATOR FUNCTION)
# -------------------------------------------------------------------
# This is the rubric's required "void function that mutates an argument"
# pattern. Notice the function name starts with `add_` not `get_`.
# Notice it does NOT return anything. It modifies snapshot directly.
#
# Run `tasklist /fo csv` and append a dict to
#   snapshot["running_processes"]
# for each process line.
#
# CSV columns from `tasklist /fo csv` (in order):
#   1. Image Name (e.g. "svchost.exe")
#   2. PID        (e.g. "1024")
#   3. Session Name (we don't need this)
#   4. Session #    (we don't need this)
#   5. Mem Usage    (we don't need this)
#
# IMPORTANT: the first row is a header row — skip it!
#
# Each entry you append should look like:
#   {
#     "pid": 1024,
#     "name": "svchost.exe",
#     "parent_pid": None,        # not available from tasklist
#     "executable_path": None,   # not available from tasklist
#     "command_line": None       # not available from tasklist
#   }
#
# Convert pid from string to int with int(). Wrap that conversion
# in try/except in case a row has a weird value.
#
# Use the csv module:
#   reader = csv.reader(output.splitlines())
#   for row in reader:
#       ...
#
# Refresher: ATBS Ch. 18 (CSV files).
# AI prompt: see Milestone 5 in the project spec.

def add_running_processes(snapshot):
    try:
        # Run tasklist in CSV format so each process row is quoted and comma-separated.
        output = run_command(["tasklist", "/fo", "csv"])
        
        # Parse the CSV output line by line using the csv module.
        reader = csv.reader(output.splitlines())
        
        # Skip the first row because it is the header row, not a process.
        first_row = True
        for row in reader:
            if first_row:
                first_row = False
                continue
            
            # Skip rows that don't have at least the required columns.
            if len(row) < 2:
                continue
            
            name = row[0].strip()
            pid_str = row[1].strip()
            
            # Convert the PID string to an integer, but don't crash if it is weird.
            try:
                pid = int(pid_str)
            except ValueError:
                pid = None
            
            # Append the process info directly into snapshot["running_processes"].
            # This mutates the list in place rather than returning a new one.
            snapshot["running_processes"].append({
                "pid": pid,
                "name": name,
                "parent_pid": None,
                "executable_path": None,
                "command_line": None
            })
    except Exception as e:
        add_warning(snapshot, "running_processes failed: " + str(e))


# -------------------------------------------------------------------
# Milestone 6 — Persistence Locations
# -------------------------------------------------------------------
# Capture entries from 4 registry keys plus 2 startup folders.
#
# Registry keys to enumerate (read ALL values under each):
#   - HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
#   - HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
#   - HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce
#   - HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce
#
# Startup folders to list (just the filenames):
#   - All-users:    %PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs\Startup
#   - Current user: %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
#
# Fields to populate in `info`:
#   - "hklm_run":       list of {"name": ..., "value": ...} dicts
#   - "hkcu_run":       list of {"name": ..., "value": ...} dicts
#   - "hklm_run_once":  list of {"name": ..., "value": ...} dicts
#   - "hkcu_run_once":  list of {"name": ..., "value": ...} dicts
#   - "all_users_startup_folder":     {"path": ..., "files": [...]}
#   - "current_user_startup_folder":  {"path": ..., "files": [...]}
#
# Helper hint:
#   You'll want a small inner helper function that takes (hive, subkey)
#   and returns a list of {"name": ..., "value": ...} dicts. Use
#   winreg.EnumValue(key, i) in a loop — it returns a tuple of
#   (name, value, value_type) and raises OSError when you've enumerated
#   all values. See the project spec for the full code pattern.
#
# Folder hint:
#   Use os.environ.get("PROGRAMDATA") and os.environ.get("APPDATA") to
#   get the base paths, then os.path.join(...) to build the full path.
#   Use os.listdir(path) to get the filenames. Wrap the listdir call
#   in try/except — the folder might not exist on a fresh system.
#
# Example of what `info` should look like when you finish:
#   {
#     "hklm_run": [
#       {"name": "SecurityHealth", "value": "%windir%\\system32\\..."},
#       ...
#     ],
#     "hkcu_run": [
#       {"name": "OneDrive", "value": "..."}
#     ],
#     "hklm_run_once": [],
#     "hkcu_run_once": [],
#     "all_users_startup_folder": {"path": "C:\\ProgramData\\...", "files": []},
#     "current_user_startup_folder": {"path": "C:\\Users\\...", "files": ["VPN.lnk"]}
#   }
#
# Refresher: ATBS Ch. 9 (file paths).
# AI prompt: see Milestone 6 in the project spec.

def get_persistence_locations(snapshot):
    info = {}
    try:
        # Helper that returns a list of name/value dicts for a registry key.
        def enumerate_values(hive, subkey):
            values = []
            try:
                key = winreg.OpenKey(hive, subkey)
                i = 0
                while True:
                    try:
                        # EnumValue returns a tuple (name, value, type) for the i-th value.
                        name, value, _ = winreg.EnumValue(key, i)
                        values.append({"name": name, "value": value})
                        i += 1
                    except OSError:
                        # No more values under this key; stop enumerating.
                        break
                winreg.CloseKey(key)
            except Exception:
                # If the key doesn't exist or can't be opened, return an empty list.
                return []
            return values

        # Enumerate each of the 4 persistence registry keys.
        info["hklm_run"] = enumerate_values(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        )
        info["hkcu_run"] = enumerate_values(
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        )
        info["hklm_run_once"] = enumerate_values(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"
        )
        info["hkcu_run_once"] = enumerate_values(
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"
        )

        # Build paths for the two Startup folders using environment variables.
        all_users_startup = os.path.join(
            os.environ.get("PROGRAMDATA", ""),
            "Microsoft",
            "Windows",
            "Start Menu",
            "Programs",
            "Startup"
        )
        current_user_startup = os.path.join(
            os.environ.get("APPDATA", ""),
            "Microsoft",
            "Windows",
            "Start Menu",
            "Programs",
            "Startup"
        )

        # List the filenames in the folder, or return an empty list if the folder is missing.
        try:
            all_files = os.listdir(all_users_startup)
        except Exception:
            all_files = []
        try:
            current_files = os.listdir(current_user_startup)
        except Exception:
            current_files = []

        info["all_users_startup_folder"] = {
            "path": all_users_startup,
            "files": all_files
        }
        info["current_user_startup_folder"] = {
            "path": current_user_startup,
            "files": current_files
        }
    except Exception as e:
        add_warning(snapshot, "persistence_locations failed: " + str(e))
    return info


# -------------------------------------------------------------------
# Milestone 7a — Network Configuration
# -------------------------------------------------------------------
# Parse `ipconfig /all` into a list of adapter dicts. This is a
# state-tracking parse — you have to remember which adapter you're
# "inside" as you walk the lines, because the lines underneath each
# adapter header belong to that adapter.
#
# Adapter header lines look like:
#     Ethernet adapter Ethernet:
#     Wireless LAN adapter Wi-Fi:
# (They end with `:` and don't start with whitespace.)
#
# Lines beneath an adapter header look like:
#     Description . . . . . . : Intel Ethernet Connection
#     Physical Address. . . . : AA-BB-CC-11-22-33
#     DHCP Enabled. . . . . . : Yes
#     IPv4 Address. . . . . . : 192.168.1.42(Preferred)
#     Subnet Mask . . . . . . : 255.255.255.0
#     Default Gateway . . . . : 192.168.1.1
#     DNS Servers . . . . . . : 192.168.1.1
#                               8.8.8.8
#
# For each adapter, build a dict with these fields:
#   - "name"             (string, from the adapter header)
#   - "description"      (string)
#   - "mac_address"      (string)
#   - "dhcp_enabled"     (boolean — True if value is "Yes")
#   - "ipv4_addresses"   (list of strings — strip any "(Preferred)" suffix)
#   - "ipv4_subnet_mask" (string or None)
#   - "default_gateway"  (string or None)
#   - "dns_servers"      (list of strings)
#
# Append each completed adapter dict to `info["adapters"]`.
# DON'T FORGET to append the LAST adapter — at the end of the loop,
# if you have a current_adapter that hasn't been appended yet, append it.
#
# State-tracking pattern (sketch — fill in the details yourself):
#   current_adapter = None
#   for line in output.split("\n"):
#       if <line is an adapter header>:
#           if current_adapter is not None:
#               info["adapters"].append(current_adapter)
#           current_adapter = {<empty adapter dict>}
#       elif ":" in line and current_adapter is not None:
#           label, _, value = line.partition(":")
#           # clean up label (strip dots and whitespace) and value
#           # store the value in the right field of current_adapter
#   if current_adapter is not None:
#       info["adapters"].append(current_adapter)
#
# Refresher: ATBS Ch. 6 (strings).
# AI prompt: see Milestone 7 in the project spec.

def get_network_configuration(snapshot):
    info = {"primary_dns_suffix": "", "adapters": []}
    try:
        # Run ipconfig /all and capture its output as text.
        output = run_command(["ipconfig", "/all"])

        # Track the adapter we're currently parsing, plus the last field
        # that can continue onto indented lines (DNS servers only).
        current_adapter = None
        current_continuation = None

        # Walk each line of the output and use the state-tracking pattern.
        for raw_line in output.splitlines():
            line = raw_line.rstrip()

            # Skip blank lines; they don't carry useful data.
            if not line:
                continue

            # Detect adapter header lines like "Ethernet adapter Ethernet:".
            if not line[0].isspace() and line.endswith(":") and "adapter" in line.lower():
                # If we were parsing an adapter already, save it before starting a new one.
                if current_adapter is not None:
                    info["adapters"].append(current_adapter)

                # Start a fresh adapter with all required fields initialized.
                current_adapter = {
                    "name": line[:-1].strip(),
                    "description": "",
                    "mac_address": "",
                    "dhcp_enabled": False,
                    "ipv4_addresses": [],
                    "ipv4_subnet_mask": None,
                    "default_gateway": None,
                    "dns_servers": []
                }
                current_continuation = None
                continue

            # If we have not yet started an adapter, look only for global info.
            if current_adapter is None:
                if ":" in line:
                    label, _, value = line.partition(":")
                    if label.strip().lower() == "primary dns suffix":
                        info["primary_dns_suffix"] = value.strip()
                continue

            # Parse labeled lines inside an adapter block.
            if ":" in line:
                label, _, value = line.partition(":")
                label = label.strip().rstrip(".").lower()
                value = value.strip()

                if label == "description":
                    current_adapter["description"] = value
                    current_continuation = None
                elif label == "physical address":
                    current_adapter["mac_address"] = value
                    current_continuation = None
                elif label == "dhcp enabled":
                    current_adapter["dhcp_enabled"] = value.lower() == "yes"
                    current_continuation = None
                elif label == "ipv4 address":
                    # Remove the optional "(Preferred)" suffix from the IP.
                    address = value.split("(")[0].strip()
                    current_adapter["ipv4_addresses"].append(address)
                    current_continuation = None
                elif label == "subnet mask":
                    current_adapter["ipv4_subnet_mask"] = value or None
                    current_continuation = None
                elif label == "default gateway":
                    current_adapter["default_gateway"] = value or None
                    current_continuation = "default_gateway"
                elif label == "dns servers":
                    if value:
                        current_adapter["dns_servers"].append(value)
                    current_continuation = "dns_servers"
                else:
                    # Unused labels are ignored; reset continuation state.
                    current_continuation = None
            else:
                # This is an indented continuation line, typically an extra DNS server.
                if current_continuation == "dns_servers":
                    current_adapter["dns_servers"].append(line.strip())
                elif current_continuation == "default_gateway" and line.strip():
                    # Some ipconfig outputs put additional default gateways on indented lines.
                    current_adapter["default_gateway"] = line.strip()

        # Append the last adapter we parsed, if any.
        if current_adapter is not None:
            info["adapters"].append(current_adapter)
    except Exception as e:
        add_warning(snapshot, "network_configuration failed: " + str(e))
    return info


# -------------------------------------------------------------------
# Milestone 7b — Listening Ports (MUTATOR FUNCTION)
# -------------------------------------------------------------------
# Like Milestone 5, this function returns nothing and adds entries
# directly to snapshot["listening_ports"].
#
# Run `netstat -ano` and append one dict per LISTENING TCP port (and
# every UDP entry, since UDP doesn't have a "state").
#
# Sample line from `netstat -ano`:
#   "  TCP    0.0.0.0:135    0.0.0.0:0    LISTENING    1024"
#
# Columns (after splitting on whitespace):
#   0: Protocol  ("TCP" or "UDP")
#   1: Local Address  ("0.0.0.0:135")
#   2: Foreign Address  (we don't need this)
#   3: State  ("LISTENING" for TCP — UDP rows don't have this)
#   4 (or last): PID  ("1024")
#
# Each entry you append should look like:
#   {
#     "protocol": "TCP",
#     "local_address": "0.0.0.0",
#     "local_port": 135,
#     "state": "LISTENING",
#     "owning_pid": 1024,
#     "owning_process_name": "svchost.exe"
#   }
#
# Filtering rules:
#   - If protocol is "TCP", only keep the row if state == "LISTENING".
#   - If protocol is "UDP", keep all rows (state should be None).
#   - Skip rows that are too short to parse (header lines, blank lines).
#
# Tip: split the local_address on the LAST colon (use .rfind(":"))
# to separate the host from the port. This handles IPv6 addresses
# like [::]:135 correctly.
#
# OPTIONAL but cool: cross-reference each PID with the output of
# `tasklist /fo csv /nh` to get the process name. Build a dictionary
# {pid: process_name} from tasklist FIRST, then look up each PID as
# you process the netstat lines.
#
# Refresher: ATBS Ch. 6 (strings) and Ch. 7 (dictionaries as lookup tables).
# AI prompt: see Milestone 7 in the project spec.

def add_listening_ports(snapshot):
    try:
        # Build a PID-to-process-name lookup from tasklist so we can
        # attach process names to the netstat results if available.
        pid_to_name = {}
        tasklist_output = run_command(["tasklist", "/fo", "csv", "/nh"])
        for row in csv.reader(tasklist_output.splitlines()):
            # Skip rows that don't have enough columns.
            if len(row) < 2:
                continue
            process_name = row[0].strip()
            pid_str = row[1].strip()
            try:
                pid = int(pid_str)
            except ValueError:
                # If PID cannot be parsed, ignore this row.
                continue
            pid_to_name[pid] = process_name

        # Run netstat to get the current network connections with PIDs.
        output = run_command(["netstat", "-ano"])
        for raw_line in output.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) < 4:
                continue

            protocol = parts[0]
            if protocol not in ("TCP", "UDP"):
                continue

            local_address = parts[1]
            pid_str = parts[-1]
            state = None
            if protocol == "TCP":
                if len(parts) < 5:
                    continue
                state = parts[3]
                if state.upper() != "LISTENING":
                    continue

            # Split on the last colon so IPv6 addresses like [::]:135 work.
            idx = local_address.rfind(":")
            if idx == -1:
                continue
            address = local_address[:idx]
            port_str = local_address[idx + 1:]
            try:
                port = int(port_str)
            except ValueError:
                continue

            try:
                pid = int(pid_str)
            except ValueError:
                pid = None

            snapshot["listening_ports"].append({
                "protocol": protocol,
                "local_address": address,
                "local_port": port,
                "state": state,
                "owning_pid": pid,
                "owning_process_name": pid_to_name.get(pid)
            })
    except Exception as e:
        add_warning(snapshot, "listening_ports failed: " + str(e))


# ===================================================================
# Milestone 8 — The Final 7 Collectors
# ===================================================================
# Every function below uses techniques you've already seen.
# Recommended order (easiest first):
#
#     1. get_network_shares          (parses `net share`, ~Milestone 3 style)
#     2. get_installed_hotfixes      (parses `wmic qfe`, CSV style)
#     3. get_local_user_accounts     (parses `net user`, ~Milestone 3 style)
#     4. get_hardware_profile        (registry + `wmic logicaldisk`)
#     5. get_security_posture        (registry + `netsh` + `manage-bde`)
#     6. get_performance_snapshot    (parses `typeperf`)
#     7. get_auto_start_services     (slowest — save for last)
#
# A note on `wmic ... /format:csv`: the output has a few quirks.
# (a) There are usually one or two blank lines at the top — strip them.
# (b) The first column is always "Node" (the hostname) — you can ignore it.
# csv.DictReader handles the parsing once you've stripped the blanks:
#
#     output = run_command(["wmic", "qfe", "get", "HotFixID,Description", "/format:csv"])
#     clean = "\n".join(line for line in output.splitlines() if line.strip())
#     reader = csv.DictReader(io.StringIO(clean))
#     for row in reader:
#         hotfix_id = row.get("HotFixID")
#         ...


# -------------------------------------------------------------------
# Milestone 8 — Hardware Profile
# -------------------------------------------------------------------
# Combines registry reads with one wmic call.
#
# Fields to populate in `info` (all dicts inside `info`):
#
# info["cpu"] = {
#   "name":               from REG HKLM\HARDWARE\DESCRIPTION\System\CentralProcessor\0\ProcessorNameString
#   "manufacturer":       from REG ...\CentralProcessor\0\VendorIdentifier
#   "max_clock_mhz":      from REG ...\CentralProcessor\0\~MHz
#   "architecture":       from PY platform.machine()
#   "logical_processors": from PY os.cpu_count()
# }
#
# info["bios"] = {
#   "manufacturer": from REG HKLM\HARDWARE\DESCRIPTION\System\BIOS\BIOSVendor
#   "version":      from REG ...\BIOS\BIOSVersion
#   "release_date": from REG ...\BIOS\BIOSReleaseDate
# }
#
# info["system"] = {
#   "manufacturer": from REG HKLM\HARDWARE\DESCRIPTION\System\BIOS\SystemManufacturer
#   "model":        from REG ...\BIOS\SystemProductName
# }
#
# info["memory"] = {
#   "total_physical_bytes": parse from `systeminfo` "Total Physical Memory: 16,384 MB"
#                           Strip the commas and " MB", convert to int, multiply by 1024 * 1024
# }
#
# info["logical_disks"] = list of dicts, one per drive, from
#   `wmic logicaldisk get DeviceID,FileSystem,Size,FreeSpace /format:csv`
#   Each entry: {
#     "drive_letter":     "C:",
#     "filesystem":       "NTFS",
#     "total_size_bytes": 511101177856,    # int — convert from string
#     "free_space_bytes": 245031440384     # int — convert from string
#   }

def get_hardware_profile(snapshot):
    info = {"cpu": {}, "memory": {}, "bios": {}, "system": {}, "logical_disks": []}
    try:
        # Read CPU info from registry.
        info["cpu"]["name"] = get_registry_value(
            winreg.HKEY_LOCAL_MACHINE,
            r"HARDWARE\DESCRIPTION\System\CentralProcessor\0",
            "ProcessorNameString"
        )
        info["cpu"]["manufacturer"] = get_registry_value(
            winreg.HKEY_LOCAL_MACHINE,
            r"HARDWARE\DESCRIPTION\System\CentralProcessor\0",
            "VendorIdentifier"
        )
        info["cpu"]["max_clock_mhz"] = get_registry_value(
            winreg.HKEY_LOCAL_MACHINE,
            r"HARDWARE\DESCRIPTION\System\CentralProcessor\0",
            "~MHz"
        )
        info["cpu"]["architecture"] = platform.machine()
        info["cpu"]["logical_processors"] = os.cpu_count()
        
        # Read BIOS info from registry.
        info["bios"]["manufacturer"] = get_registry_value(
            winreg.HKEY_LOCAL_MACHINE,
            r"HARDWARE\DESCRIPTION\System\BIOS",
            "BIOSVendor"
        )
        info["bios"]["version"] = get_registry_value(
            winreg.HKEY_LOCAL_MACHINE,
            r"HARDWARE\DESCRIPTION\System\BIOS",
            "BIOSVersion"
        )
        info["bios"]["release_date"] = get_registry_value(
            winreg.HKEY_LOCAL_MACHINE,
            r"HARDWARE\DESCRIPTION\System\BIOS",
            "BIOSReleaseDate"
        )
        
        # Read system info from registry.
        info["system"]["manufacturer"] = get_registry_value(
            winreg.HKEY_LOCAL_MACHINE,
            r"HARDWARE\DESCRIPTION\System\BIOS",
            "SystemManufacturer"
        )
        info["system"]["model"] = get_registry_value(
            winreg.HKEY_LOCAL_MACHINE,
            r"HARDWARE\DESCRIPTION\System\BIOS",
            "SystemProductName"
        )
        
        # Get memory info from systeminfo command.
        systeminfo_output = run_command(["systeminfo"])
        for line in systeminfo_output.splitlines():
            if "Total Physical Memory:" in line:
                # Parse the value like "16,384 MB".
                _, _, value = line.partition(":")
                value = value.strip().replace(",", "").replace(" MB", "")
                try:
                    mb = int(value)
                    info["memory"]["total_physical_bytes"] = mb * 1024 * 1024
                except ValueError:
                    pass
                break
        
        # Get logical disks from wmic.
        disk_output = run_command([
            "wmic", "logicaldisk", "get", "DeviceID,FileSystem,Size,FreeSpace", "/format:csv"
        ])
        clean_disk_output = "\n".join(line for line in disk_output.splitlines() if line.strip())
        reader = csv.DictReader(io.StringIO(clean_disk_output))
        for row in reader:
            device_id = row.get("DeviceID")
            filesystem = row.get("FileSystem")
            size_str = row.get("Size")
            free_space_str = row.get("FreeSpace")
            
            try:
                size = int(size_str) if size_str else None
            except ValueError:
                size = None
            try:
                free_space = int(free_space_str) if free_space_str else None
            except ValueError:
                free_space = None
            
            if device_id:
                info["logical_disks"].append({
                    "drive_letter": device_id,
                    "filesystem": filesystem,
                    "total_size_bytes": size,
                    "free_space_bytes": free_space
                })
    except Exception as e:
        add_warning(snapshot, "hardware_profile failed: " + str(e))
    return info


# -------------------------------------------------------------------
# Milestone 8 — Local User Accounts
# -------------------------------------------------------------------
# Three pieces, all from `net` commands:
#
# info["current_user"]: from CMD `whoami` (the result is a single line,
#   like "DESKTOP-A1B2C3\\student01"). Use .strip() to remove the newline.
#
# info["users"]: list of dicts. Build it in two steps.
#   Step 1: run `net user` to get the list of usernames. The user list
#           appears between two lines of dashes. Each row can hold up
#           to 3 usernames separated by whitespace.
#   Step 2: for each username, run `net user <username>` and parse the
#           "Label:  value" lines. Fields to capture:
#             - "username":            the name itself
#             - "full_name":           from "Full Name" line
#             - "disabled":            True if "Account active" line says "No"
#             - "password_required":   True if "Password required" says "Yes"
#             - "password_changeable": True if "User may change password" says "Yes"
#             - "password_expires":    False if "Password expires" line says "Never", else True
#
# info["administrators_group_members"]: list of strings.
#   From CMD `net localgroup Administrators`. The member list is between
#   two lines of dashes (like the user list). Each member is on its
#   own line. Skip blank lines and the "The command completed" line.

def get_local_user_accounts(snapshot):
    info = {"current_user": "", "users": [], "administrators_group_members": []}
    try:
        # Get the current user from whoami.
        whoami_output = run_command(["whoami"])
        info["current_user"] = whoami_output.strip()
        
        # Get the list of all users from net user.
        net_user_output = run_command(["net", "user"])
        
        # Extract usernames from the output (between dashes).
        usernames = []
        in_user_list = False
        for line in net_user_output.splitlines():
            line = line.strip()
            if line.startswith("-") and line.endswith("-"):
                in_user_list = True
                continue
            if "command completed" in line.lower():
                break
            if in_user_list and line:
                # Each line can have multiple usernames separated by spaces.
                usernames.extend(line.split())
        
        # For each username, get detailed info.
        for username in usernames:
            user_info = {"username": username}
            
            # Run net user <username> to get details.
            user_detail_output = run_command(["net", "user", username])
            
            # Parse the "Label: value" lines.
            for line in user_detail_output.splitlines():
                line = line.strip()
                if ":" in line:
                    label, _, value = line.partition(":")
                    label = label.strip()
                    value = value.strip()
                    
                    if label == "Full Name":
                        user_info["full_name"] = value
                    elif label == "Account active":
                        user_info["disabled"] = value.lower() == "no"
                    elif label == "Password required":
                        user_info["password_required"] = value.lower() == "yes"
                    elif label == "User may change password":
                        user_info["password_changeable"] = value.lower() == "yes"
                    elif label == "Password expires":
                        user_info["password_expires"] = value.lower() != "never"
            
            # Append the user dict.
            info["users"].append(user_info)
        
        # Get the administrators group members.
        admin_output = run_command(["net", "localgroup", "Administrators"])
        
        # Extract members from the output (between dashes).
        in_admin_list = False
        for line in admin_output.splitlines():
            line = line.strip()
            if line.startswith("-") and line.endswith("-"):
                in_admin_list = True
                continue
            if "command completed" in line.lower():
                break
            if in_admin_list and line and not line.startswith("*"):
                # Remove leading * if present.
                member = line.lstrip("*").strip()
                info["administrators_group_members"].append(member)
    except Exception as e:
        add_warning(snapshot, "local_user_accounts failed: " + str(e))
    return info


# -------------------------------------------------------------------
# Milestone 8 — Auto-Start Services
# -------------------------------------------------------------------
# This one is the slowest collector — it can take 30+ seconds.
#
# Strategy:
#   Step 1: run `sc query` to get a list of all services. The output
#           is grouped in blocks like:
#               SERVICE_NAME: BITS
#               DISPLAY_NAME: Background Intelligent Transfer Service
#                       TYPE               : 20  WIN32_SHARE_PROCESS
#                       STATE              : 4  RUNNING
#                       ...
#           For each block, capture the service name, display name, and state.
#
#   Step 2: for each service name, run `sc qc <name>` to get its config.
#           Capture START_TYPE, BINARY_PATH_NAME, SERVICE_START_NAME.
#
#   Step 3: ONLY if START_TYPE contains "AUTO_START", append a dict to
#           the `services` list:
#             {
#               "name":            "BITS",
#               "display_name":    "Background Intelligent Transfer Service",
#               "state":           "RUNNING",
#               "start_type":      "Auto",
#               "executable_path": "C:\\Windows\\system32\\svchost.exe -k netsvcs -p",
#               "log_on_as":       "LocalSystem"
#             }

def get_auto_start_services(snapshot):
    services = []
    try:
        # Run sc query to get all services.
        query_output = run_command(["sc", "query"])
        
        # Parse the output to extract service names.
        service_names = []
        current_service = {}
        for line in query_output.splitlines():
            line = line.strip()
            if line.startswith("SERVICE_NAME:"):
                if current_service:
                    service_names.append(current_service["name"])
                current_service = {"name": line.split(":", 1)[1].strip()}
            elif line.startswith("DISPLAY_NAME:"):
                current_service["display_name"] = line.split(":", 1)[1].strip()
            elif line.startswith("STATE"):
                current_service["state"] = line.split(":", 1)[1].strip().split()[1]
        
        # Don't forget the last one.
        if current_service:
            service_names.append(current_service["name"])
        
        # For each service, get its config with sc qc.
        for name in service_names:
            qc_output = run_command(["sc", "qc", name])
            
            start_type = None
            binary_path = None
            log_on_as = None
            
            for line in qc_output.splitlines():
                line = line.strip()
                if line.startswith("START_TYPE"):
                    start_type = line.split(":", 1)[1].strip()
                elif line.startswith("BINARY_PATH_NAME"):
                    binary_path = line.split(":", 1)[1].strip()
                elif line.startswith("SERVICE_START_NAME"):
                    log_on_as = line.split(":", 1)[1].strip()
            
            # Only include auto-start services.
            if start_type and "AUTO" in start_type.upper():
                services.append({
                    "name": name,
                    "display_name": current_service.get("display_name", ""),
                    "state": current_service.get("state", ""),
                    "start_type": start_type,
                    "executable_path": binary_path,
                    "log_on_as": log_on_as
                })
    except Exception as e:
        add_warning(snapshot, "auto_start_services failed: " + str(e))
    return services


# -------------------------------------------------------------------
# Milestone 8 — Installed Hotfixes
# -------------------------------------------------------------------
# Run:
#   wmic qfe get HotFixID,Description,InstalledOn,InstalledBy /format:csv
#
# Strip blank lines from the output, then parse with csv.DictReader.
#
# Each entry you append should look like:
#   {
#     "hotfix_id":    "KB5034123",
#     "description":  "Security Update",
#     "installed_on": "5/4/2026",       # leave as-is, or normalize to ISO if you want
#     "installed_by": "NT AUTHORITY\\SYSTEM"
#   }

def get_installed_hotfixes(snapshot):
    hotfixes = []
    try:
        # Run wmic to get hotfix information in CSV format.
        output = run_command([
            "wmic", "qfe", "get", "HotFixID,Description,InstalledOn,InstalledBy", "/format:csv"
        ])
        
        # Clean the output by removing blank lines.
        clean_output = "\n".join(line for line in output.splitlines() if line.strip())
        
        # Parse the CSV using DictReader.
        reader = csv.DictReader(io.StringIO(clean_output))
        
        # Skip the first row if it's the header (Node,HotFixID,...).
        for row in reader:
            # Ignore the Node column (always the hostname).
            hotfix_id = row.get("HotFixID")
            description = row.get("Description")
            installed_on = row.get("InstalledOn")
            installed_by = row.get("InstalledBy")
            
            # Only append if we have at least a hotfix ID.
            if hotfix_id:
                hotfixes.append({
                    "hotfix_id": hotfix_id,
                    "description": description,
                    "installed_on": installed_on,
                    "installed_by": installed_by
                })
    except Exception as e:
        add_warning(snapshot, "installed_hotfixes failed: " + str(e))
    return hotfixes


# -------------------------------------------------------------------
# Milestone 8 — Scheduled Tasks
# -------------------------------------------------------------------
# Run:
#   schtasks /query /fo csv /v
#
# Note: this command can take 30+ seconds on some systems. Be patient.
# Note: the timeout in run_command() is 30s. If you hit timeouts here,
# you can call subprocess.run() directly with a longer timeout for
# this one collector.
#
# Parse the CSV with csv.DictReader. The output has many columns, but
# you only need:
#   - "TaskName"
#   - "Status"
#   - "Next Run Time"
#   - "Last Run Time"
#   - "Last Result"
#   - "Author"
#   - "Task To Run"
#
# Two filtering rules:
#   - schtasks repeats the header row for each task folder — skip any
#     row where TaskName == "TaskName" or TaskName is empty.
#   - To keep noise down, skip any task whose name starts with
#     "\\Microsoft\\Windows\\" — those are built-in tasks that exist
#     on every Windows system.
#
# Each entry: { "task_name": ..., "status": ..., ... }

def get_scheduled_tasks(snapshot):
    tasks = []
    try:
        # TODO Milestone 8: parse `schtasks /query /fo csv /v` and append
        # one dict per non-Microsoft task.
        pass
    except Exception as e:
        add_warning(snapshot, "scheduled_tasks failed: " + str(e))
    return tasks


# -------------------------------------------------------------------
# Milestone 8 — Security Posture
# -------------------------------------------------------------------
# Three sub-blocks. Each is independent — implement one at a time.
#
# A) info["firewall"]
#    For each of the 3 profiles (domain, private, public), run:
#       netsh advfirewall show <profile>profile
#    Build a dict with two fields:
#       - "state": "ON" or "OFF" (from the "State" line)
#       - "logging_dropped_connections": True/False (from "LogDroppedConnections")
#    Store under info["firewall"]["domain_profile"], etc.
#
# B) info["uac"]
#    Read 3 values from the registry under
#       HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System
#    Build:
#       {
#         "enabled": True if EnableLUA == 1,
#         "consent_prompt_behavior_admin": ConsentPromptBehaviorAdmin (int),
#         "prompt_on_secure_desktop": True if PromptOnSecureDesktop == 1
#       }
#
# C) info["bitlocker"]
#    Run `manage-bde -status C:`. This requires Administrator rights —
#    if the script isn't elevated, the command returns nothing and you
#    should call add_warning() to note that.
#    Parse these labeled lines:
#       - "Protection Status" → info["bitlocker"]["system_drive_protection_status"]
#       - "Encryption Method" → info["bitlocker"]["encryption_method"]
#       - line containing "percentage encrypted" → info["bitlocker"]["encryption_percentage"]
#         (strip the "%" sign and convert to float)
#    If manage-bde returned nothing, leave all 3 fields as None.

def get_security_posture(snapshot):
    info = {"firewall": {}, "uac": {}, "bitlocker": {}}
    try:
        # Firewall: check each profile.
        profiles = ["domain", "private", "public"]
        for profile in profiles:
            firewall_output = run_command(["netsh", "advfirewall", "show", f"{profile}profile"])
            
            profile_info = {"state": "OFF", "logging_dropped_connections": False}
            for line in firewall_output.splitlines():
                if "State" in line and ":" in line:
                    _, _, state = line.partition(":")
                    profile_info["state"] = state.strip().upper()
                elif "LogDroppedConnections" in line and ":" in line:
                    _, _, logging = line.partition(":")
                    profile_info["logging_dropped_connections"] = logging.strip().lower() == "enable"
            
            info["firewall"][f"{profile}_profile"] = profile_info
        
        # UAC: read from registry.
        enable_lua = get_registry_value(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
            "EnableLUA"
        )
        consent_behavior = get_registry_value(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
            "ConsentPromptBehaviorAdmin"
        )
        prompt_desktop = get_registry_value(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
            "PromptOnSecureDesktop"
        )
        
        info["uac"]["enabled"] = enable_lua == 1
        info["uac"]["consent_prompt_behavior_admin"] = consent_behavior
        info["uac"]["prompt_on_secure_desktop"] = prompt_desktop == 1
        
        # BitLocker: run manage-bde.
        bitlocker_output = run_command(["manage-bde", "-status", "C:"])
        
        if bitlocker_output.strip():
            for line in bitlocker_output.splitlines():
                line = line.strip()
                if "Protection Status:" in line:
                    _, _, status = line.partition(":")
                    info["bitlocker"]["system_drive_protection_status"] = status.strip()
                elif "Encryption Method:" in line:
                    _, _, method = line.partition(":")
                    info["bitlocker"]["encryption_method"] = method.strip()
                elif "percentage encrypted" in line.lower():
                    # Extract the percentage.
                    parts = line.split()
                    for part in parts:
                        if "%" in part:
                            try:
                                percent = float(part.strip("%"))
                                info["bitlocker"]["encryption_percentage"] = percent
                            except ValueError:
                                pass
                            break
        else:
            # If no output, assume not elevated or not configured.
            add_warning(snapshot, "bitlocker status requires Administrator rights")
    except Exception as e:
        add_warning(snapshot, "security_posture failed: " + str(e))
    return info


# -------------------------------------------------------------------
# Milestone 8 — Performance Snapshot
# -------------------------------------------------------------------
# Sample 5 performance counters using `typeperf`. The basic call is:
#       typeperf "<counter path>" -sc 1
#
# typeperf prints a CSV-style header, then one data row. The data row
# starts with " " followed by a quoted timestamp, then the counter value.
#
# Sample output:
#   "(PDH-CSV 4.0)","\\HOST\Processor(_Total)\% Processor Time"
#   "05/04/2026 14:23:01.123","2.847"
#   Exiting, please wait...
#   The command completed successfully.
#
# A small helper makes this much easier:
#   def get_counter(counter_path):
#       output = run_command(["typeperf", counter_path, "-sc", "1"])
#       for line in output.split("\n"):
#           line = line.strip()
#           if line.startswith('"') and "," in line:
#               parts = line.split(",")
#               if len(parts) >= 2:
#                   try:
#                       return float(parts[1].strip().strip('"'))
#                   except ValueError:
#                       pass
#       return None
#
# Counters to sample (and where each value goes):
#   r"\Processor(_Total)\% Processor Time"           → cpu_total_percent (round to 2 decimals)
#   r"\Memory\Available MBytes"                      → memory.available_bytes (multiply by 1024 * 1024)
#   r"\PhysicalDisk(_Total)\Disk Reads/sec"          → disk_system_volume.reads_per_sec
#   r"\PhysicalDisk(_Total)\Disk Writes/sec"         → disk_system_volume.writes_per_sec
#   r"\System\Processes"                             → process_count (int)

def get_performance_snapshot(snapshot):
    info = {
        "sample_timestamp_utc": datetime.datetime.utcnow().isoformat() + "Z",
        "cpu_total_percent": None,
        "memory": {"available_bytes": None},
        "disk_system_volume": {"reads_per_sec": None, "writes_per_sec": None},
        "process_count": None,
    }
    try:
        # Helper to extract a counter value from typeperf output.
        def get_counter(counter_path):
            output = run_command(["typeperf", counter_path, "-sc", "1"])
            for line in output.splitlines():
                line = line.strip()
                if line.startswith('"') and "," in line:
                    parts = line.split(",")
                    if len(parts) >= 2:
                        try:
                            return float(parts[1].strip().strip('"'))
                        except ValueError:
                            pass
            return None
        
        # Sample each counter.
        cpu_percent = get_counter(r"\Processor(_Total)\% Processor Time")
        if cpu_percent is not None:
            info["cpu_total_percent"] = round(cpu_percent, 2)
        
        memory_mb = get_counter(r"\Memory\Available MBytes")
        if memory_mb is not None:
            info["memory"]["available_bytes"] = int(memory_mb * 1024 * 1024)
        
        disk_reads = get_counter(r"\PhysicalDisk(_Total)\Disk Reads/sec")
        info["disk_system_volume"]["reads_per_sec"] = disk_reads
        
        disk_writes = get_counter(r"\PhysicalDisk(_Total)\Disk Writes/sec")
        info["disk_system_volume"]["writes_per_sec"] = disk_writes
        
        process_count = get_counter(r"\System\Processes")
        if process_count is not None:
            info["process_count"] = int(process_count)
    except Exception as e:
        add_warning(snapshot, "performance_snapshot failed: " + str(e))
    return info


# -------------------------------------------------------------------
# Milestone 8 — Network Shares
# -------------------------------------------------------------------
# Run `net share`. Output looks like:
#
#   Share name   Resource                   Remark
#   -------------------------------------------------------------
#   ADMIN$       C:\Windows                 Remote Admin
#   C$           C:\                        Default share
#   IPC$                                    Remote IPC
#   The command completed successfully.
#
# The data rows are between the dashes line and the "command completed" line.
# Columns are separated by 2 or more spaces (NOT tabs, NOT a single space —
# `local_path` can contain single spaces). The simplest approach: use
# the regex module's `re.split(r"\s{2,}", line.strip())`.
#
# Each entry:
#   {
#     "share_name":        "ADMIN$",
#     "local_path":        "C:\\Windows",
#     "description":       "Remote Admin",
#     "is_administrative": True   # True if share_name ends with "$"
#   }
#
# (The simplest collector in Milestone 8. Start here.)

def get_network_shares(snapshot):
    shares = []
    try:
        # Run net share to get the list of shared resources.
        output = run_command(["net", "share"])
        
        # Track whether we're inside the data section (between dashes and completion message).
        in_data_section = False
        
        # Walk each line of the output.
        for line in output.splitlines():
            line = line.strip()
            
            # Skip empty lines.
            if not line:
                continue
            
            # Detect the start of the data section (the dashes line).
            if line.startswith("-") and line.endswith("-"):
                in_data_section = True
                continue
            
            # Detect the end of the data section (completion message).
            if "command completed" in line.lower():
                break
            
            # If we're in the data section, parse the line.
            if in_data_section:
                # Split on 2 or more spaces to separate columns.
                # Use re.split to handle variable whitespace.
                import re
                parts = re.split(r"\s{2,}", line)
                
                # Expect at least 2 parts: share name and resource.
                if len(parts) >= 2:
                    share_name = parts[0]
                    local_path = parts[1] if len(parts) > 1 else ""
                    description = parts[2] if len(parts) > 2 else ""
                    
                    # Determine if it's an administrative share (ends with $).
                    is_administrative = share_name.endswith("$")
                    
                    # Append the share dict.
                    shares.append({
                        "share_name": share_name,
                        "local_path": local_path,
                        "description": description,
                        "is_administrative": is_administrative
                    })
    except Exception as e:
        add_warning(snapshot, "network_shares failed: " + str(e))
    return shares
