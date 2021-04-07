import subprocess, sys

p = subprocess.Popen(
    ["powershell.exe", "cd c:/ ; dir ; & 'C:/Program Files/Notepad++/notepad++.exe'"],
    # "cd c:/ & dir",
    stdout=sys.stdout,
    # shell=True,
    # executable= "c:/windows/system32/cmd.exe",
    # cwd="c:/"
    )
p.communicate()

