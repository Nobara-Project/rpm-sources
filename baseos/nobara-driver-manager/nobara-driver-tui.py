#!/usr/bin/python3
import json
import subprocess
import os
import sys
import urllib.request
import shutil

PURPLE = "#a665ce"

os.environ["PATH"] += os.pathsep + "/usr/local/bin" + os.pathsep + "/usr/bin"
if "TERM" not in os.environ:
    os.environ["TERM"] = "xterm-256color"

def fetch_profiles():
    profiles = []
    sources = [
        ("pci", "https://raw.githubusercontent.com/Nobara-Project/cfhdb/refs/heads/master/data/profiles/pci.json"),
        ("usb", "https://raw.githubusercontent.com/Nobara-Project/cfhdb/refs/heads/master/data/profiles/usb.json")
    ]
    for p_type, url in sources:
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())
                for p in data.get('profiles', []):
                    p['source_type'] = p_type 
                    profiles.append(p)
        except Exception: pass

    profiles.sort(key=lambda x: x.get('codename', '').lower())
    return profiles

def check_installed(profile):
    codename = profile['codename']
    if os.path.exists(f"/etc/cfhdb/applied/{codename}"): return True
    check_script = profile.get('check_script', "false")
    if check_script and check_script not in ["Option::is_none", "false"]:
        try:
            res = subprocess.run(["/bin/bash", "-c", check_script], capture_output=True)
            return res.returncode == 0
        except: return False
    return False

def main():
    script_path = os.path.abspath(__file__)
    if os.geteuid() != 0:
        elevator = shutil.which("pkexec") or shutil.which("sudo")
        if elevator:
            os.execvp(elevator, [elevator, sys.executable, script_path] + sys.argv[1:])
            sys.exit(0)

    gum_path = shutil.which("gum")
    print(">>> Fetching profiles...")
    all_profiles = fetch_profiles()

    if not all_profiles:
        subprocess.run([
            gum_path, "style", "--foreground", "1", "--border", "double", 
            "--margin", "1", "--padding", "1 2", 
            "ERROR: Could not reach GitHub.\nPlease check your internet connection."
        ])
        sys.exit(1)

    while True:
        sys.stdout.write("\033[H\033[2J")
        sys.stdout.flush()

        try:
            mode = subprocess.check_output([
                gum_path, "choose", "--header", "Nobara Driver Manager",
                "--cursor.foreground", PURPLE, "Install", "Remove", "Exit"
            ], text=True).strip()
        except subprocess.CalledProcessError: break 

        if mode == "Exit": break
        is_install = mode == "Install"

        options = []
        for p in all_profiles:
            if not is_install and not p.get('removable', True): continue
            is_installed = check_installed(p)

            if not is_install and not is_installed: continue

            if is_install:
                if is_installed:
                    label = f"✔ | {p['codename']} | {p['i18n_desc']}"
                    options.insert(0, label) # Push to top
                else:
                    label = f"{p['codename']} - {p['i18n_desc']}"
                    options.append(label)
            else:
                label = f"{p['codename']} - {p['i18n_desc']}"
                options.append(label)

        try:
            selected = subprocess.check_output([
                gum_path, "filter", "--no-limit", "--header", "TAB: Select | CTRL+A: All | ESC: Back",
                "--indicator", ">", "--indicator.foreground", PURPLE,
                "--placeholder", "Search drivers..."
            ], input="\n".join(options), text=True).splitlines()
        except subprocess.CalledProcessError: continue

        for line in selected:
            if "✔ | " in line:
                codename = line.split(" | ")[1]
            else:
                codename = line.split(" - ")[0]

            profile = next(p for p in all_profiles if p['codename'] == codename)
            flag = ("-ipp" if is_install else "-upp") if profile['source_type'] == "pci" else ("-iup" if is_install else "-uup")

            subprocess.run([
                gum_path, "style", "--foreground", PURPLE, "--border", "rounded",
                "--margin", "1", "--padding", "1 2", f"Processing: {codename} ({flag})"
            ])
            subprocess.run(["cfhdb", flag, codename], stdout=None, stderr=None)

        try:
            subprocess.check_call([gum_path, "confirm", "Done. Return to menu?"])
        except subprocess.CalledProcessError:
            sys.exit(0)

if __name__ == "__main__":
    main()
