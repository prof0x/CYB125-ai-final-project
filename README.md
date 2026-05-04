# Windows Baseline Configuration Snapshot Collector
## CYB 125 Final Project — Part 1: Project Plan

**Student name:** Veysel Cetiner
**Date:** May 4, 2026

---

## What This Project Is

A Windows baseline snapshot is a structured record of how a system is configured at one moment in time — what software is installed, which services are running, who the local users are, what network ports are open, and so on. My script will collect all of that information from the Windows VM it runs on and save it as a single JSON file. The reason this matters for cybersecurity is that the JSON file from today can be compared against a future JSON file from the same machine to detect changes. If a new program shows up under a Run registry key overnight, or a new local administrator account appears, or a port that wasn't listening yesterday is listening today, the diff between the two snapshots makes that change visible. Without a baseline, a defender has nothing to compare against and unauthorized changes blend in with everything else on the system.

---

## Approach

I will gather data from three categories of sources:

- Windows Registry (read with the `winreg` Python module)
- Performance counters (sampled with the `typeperf` command)
- Command-line utilities (invoked from Python with `subprocess`)

---

## Strategy

I plan to use AI as a tutor first and a coding assistant second. My default question shape will be "explain how X works" or "walk me through Y," not "write me a function that does Z" — I want to be able to defend every line in my final script, and I know from experience that I retain code I wrote myself much better than code I pasted in. I expect AI to be most useful in Milestone 7 (the `ipconfig /all` parser), because the state-tracking pattern is new to me and I need to see it explained in plain English before I can write it; I expect to rely on AI least in Milestones 3 and 4, which are just `.split()` loops and registry walks that I should be able to write from memory after re-reading ATBS Ch. 6 and 7. To verify AI output, I will run `python main.py` after every change, open the resulting JSON file, and check that the section I just worked on contains values that match what I see when I run the underlying Windows command directly at the terminal. If the AI gives me a registry path or command flag that doesn't seem to exist on my VM, I will check Microsoft's documentation before assuming the AI is right and the documentation is wrong.

Three prompts I plan to use:

1. *"Walk me through how `winreg.EnumKey` raises `OSError` when there are no more subkeys, and how I should structure my `while True` loop around that. Don't write the full function for me yet."*
2. *"My `netstat -ano` output has IPv6 addresses like `[::]:135` mixed in with IPv4 addresses like `0.0.0.0:135`. How do I split a local address into a host and a port without accidentally splitting on the colons inside an IPv6 address? Just explain the approach — I'll write the code myself."*
3. *"I'm getting a `KeyError: 'Minimum password length'` even though I can see that exact string in the `net accounts` output when I run it at the terminal. What are the three most common reasons a Python dict lookup would fail when the key looks visually identical to what's in the source data?"*

---

## Data Dictionary Skeleton

The 16 sections that my script will produce in its output JSON file are listed below. The exact field names within each section will be designed during the matching milestone.

### 1. snapshot_metadata
When, where, and by whom this snapshot was created — including hostname, username, timestamp, and whether the script was run as Administrator.

### 2. system_identity
OS name, version, build number, install date, and whether the machine is part of a domain.

### 3. hardware_profile
CPU model and core count, total RAM, BIOS information, system manufacturer, and the list of logical disks with their sizes and free space.

### 4. network_configuration
Each network adapter's name, description, MAC address, IPv4 address, subnet mask, default gateway, and DNS servers.

### 5. listening_ports
Every TCP port the system is listening on and every UDP port it has open, including the protocol, port number, and the process ID that owns the port.

### 6. local_user_accounts
All local user accounts with their attributes (disabled, password required, etc.) plus the members of the local Administrators group.

### 7. password_policy
The system's account-level password and lockout rules — minimum length, maximum age, lockout threshold, and so on.

### 8. auto_start_services
The list of Windows services configured to launch automatically at boot, with their executable paths and the account they run as.

### 9. running_processes
A snapshot of every process that was running at the moment the baseline was collected, with PID and process name.

### 10. installed_software
Every installed application registered under the Uninstall registry hive, with name, version, and publisher.

### 11. installed_hotfixes
Every Windows update / hotfix (KB number) installed on the machine, with description and install date.

### 12. persistence_locations
The four most common registry Run/RunOnce keys plus the two Startup folders — the locations where malware most often hides to survive a reboot.

### 13. scheduled_tasks
Every scheduled task on the system (excluding noisy built-in Microsoft tasks), including author, last run, and next run.

### 14. security_posture
Windows Firewall state for each profile, UAC configuration from the registry, and BitLocker status for the system drive.

### 15. performance_snapshot
Instantaneous CPU usage, available memory, disk read/write rates, and process count at the moment of collection.

### 16. network_shares
Every SMB share the system exposes, including administrative shares ending in `$`.

---

## Notes for the Instructor

I read SKILLS.md before writing the strategy section above and I plan to follow the five habits described there. One small thing I want to flag: my VM is a fresh Windows 11 Enterprise install on the VLE, and a quick test confirms that `wmic` is still available on this image — so I plan to use it in Milestone 8 as the spec describes. If that changes when I actually start writing the collectors, I'll let you know and switch to an alternative.