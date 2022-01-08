import re
import subprocess

def get_wifi_passwords():
    '''
    Can be used only on Windows OS\n
    This function is created to find out all the internet passwords of respective connections stored on the device.\n
    '''
    INTERNET_NAME_RE = re.compile(r"\bAll User Profile\s+:\s*(?P<name>.+?)\r")
    PASSWORD_RE = re.compile(r"\bKey Content\s*:(?P<password>.+?)\r")
    result = [] # list of resultant (name, password) tuples
    
    a = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode("utf-8")
    match_iter = INTERNET_NAME_RE.finditer(a)
    names = [match.group(1) for match in match_iter]
    
    for name in names:
        password = ""
        out = subprocess.check_output(["netsh", "wlan", "show", "profile", name, "key=clear"]).decode("utf-8")
        match = PASSWORD_RE.search(out)

        if match:
            password = match.group('password')

        result.append((name, password))
        
    return result

a = get_wifi_passwords()

print("{:<30}|  {:<}".format('Name', 'Password'))
print("-"*60)

for item in a:
    name, password = item
    print("{:<30}|  {:<}".format(name, password))