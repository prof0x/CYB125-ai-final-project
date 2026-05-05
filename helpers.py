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
        # Define the registry location where Windows stores system identity info.
        # HKEY_LOCAL_MACHINE is the root hive for machine-wide settings (not user-specific).
        hive = winreg.HKEY_LOCAL_MACHINE
        # The 'r' prefix makes this a raw string — backslashes are treated as literal
        # characters instead of escape sequences (important for Windows paths).
        subkey = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
        
        # Read OS name (e.g., "Windows 11 Enterprise"). This is what you see in Settings > About.
        # Note: we store it as-is from the registry; no conversion needed.
        info["os_name"] = get_registry_value(hive, subkey, "ProductName")
        
        # Read OS build number (e.g., "22631"). Each Windows update increments this.
        # Stored as a string even though it looks like a number.
        info["os_build"] = get_registry_value(hive, subkey, "CurrentBuild")
        
        # Read OS edition (e.g., "Enterprise", "Professional"). Different editions have
        # different features and security capabilities.
        info["os_edition"] = get_registry_value(hive, subkey, "EditionID")
        
        # Read registered owner (e.g., "Acme Corp"). Used for hardware inventory and
        # ownership tracking. You could also get this from getpass.getuser() or
        # socket.gethostname(), but the registry value is the "official" owner field.
        info["registered_owner"] = get_registry_value(hive, subkey, "RegisteredOwner")
        
        # Read InstallDate. This is stored in the registry as a Unix timestamp
        # (integer seconds since January 1, 1970 UTC), which is not human-readable.
        install_epoch = get_registry_value(hive, subkey, "InstallDate")
        
        # Convert the Unix timestamp to an ISO 8601 string for the JSON report.
        # We guard against None because if the registry key doesn't exist,
        # get_registry_value() returns None, and utcfromtimestamp(None) would crash.
        if install_epoch is not None:
            # datetime.utcfromtimestamp() converts the epoch to a datetime object.
            # .isoformat() converts that object to a string like "2025-08-14T03:11:02.123456"
            # + "Z" appends the UTC timezone indicator (Z = Zulu = UTC).
            # Note: If you wanted local time instead of UTC, you could use fromtimestamp()
            # instead of utcfromtimestamp() — but we use UTC for consistency in security reports.
            info["install_date_utc"] = datetime.datetime.utcfromtimestamp(install_epoch).isoformat() + "Z"
        else:
            # If the registry value doesn't exist (shouldn't happen on normal Windows),
            # set it to None. This way the key still exists in the JSON, but with an empty value.
            info["install_date_utc"] = None
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
        # TODO Milestone 3: parse `net accounts` and populate the 7 fields
        # listed in the comment block above. Use run_command() to invoke
        # the command, then walk its output line by line.
        pass
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
        # TODO Milestone 4: walk the Uninstall hive and append a dict
        # for each program with a DisplayName.
        pass
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
        # TODO Milestone 5: parse `tasklist /fo csv` and append one dict
        # per process to snapshot["running_processes"].
        # Remember: this function does NOT return anything.
        pass
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
        # TODO Milestone 6: enumerate the 4 Run/RunOnce keys and list
        # the contents of the 2 Startup folders.
        pass
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
        # TODO Milestone 7a: parse `ipconfig /all` into a list of adapter
        # dicts as described above.
        pass
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
        # TODO Milestone 7b: parse `netstat -ano` and append one dict per
        # listening port to snapshot["listening_ports"].
        # Remember: this function does NOT return anything.
        pass
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
        # TODO Milestone 8: implement the registry reads and the wmic
        # logicaldisk call as described above.
        pass
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
        # TODO Milestone 8: implement the three pieces described above.
        pass
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
        # TODO Milestone 8: enumerate services with `sc query`, then call
        # `sc qc <name>` on each one and keep only the auto-start services.
        pass
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
        # TODO Milestone 8: parse `wmic qfe ... /format:csv` and append
        # one dict per hotfix.
        pass
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
        # TODO Milestone 8: implement the three sub-blocks (firewall,
        # uac, bitlocker) as described above.
        pass
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
        # TODO Milestone 8: sample the 5 typeperf counters described above
        # and store the results in `info`.
        pass
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
        # TODO Milestone 8: parse `net share` and append one dict per share.
        pass
    except Exception as e:
        add_warning(snapshot, "network_shares failed: " + str(e))
    return shares
