#helper file
from dataclasses import dataclass

@dataclass
class Component:
    username: str
    algorithm : str
    workfactor : str
    salt: str
    hashval : str

# make a shadow entry by parsing the shadow txt
def parse(line):
    line = line.strip()

    # split the username & scrambled word list at the ":"
    username, str1 = line.split(':')

    # split the password at the $ parts
    parts = str1.split("$") # starts off with for ex "$2b$08$" then the rest of hash / salt

    algorithm = parts[1]
    workfactor = parts[2]
    # has salt & hash
    salt_hash = parts[3]

    # given the bcrypt algorithm the first 22 chars
    # are the salt & anything after is the hash
    salt = salt_hash[:22]
    hashval = salt_hash[22:]

    return Component(username, algorithm, workfactor, salt, hashval)

def load_shadow(file):
    components = []
    with open(file, "r") as f:
        for line in f: #loop over shadow.txt
            if not line.strip(): # if line is empty go to next line
                continue
            entry = parse(line) #parse the entry
            components.append(entry) # add to component list to return
    return components