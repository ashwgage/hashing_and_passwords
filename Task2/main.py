import bcrypt
import nltk
from nltk.corpus import words
nltk.download('words')
import Shadow_Parse
from multiprocessing import Pool # for parallel processing
import time # for keeping track of how long it takes to crack each password

#getting the wordlist from nltk word database
# only getting between 6-10 words as given in the instructions
nltk_wordlist = [w for w in words.words() if 6 <= len(w) <= 10]

#Task

"""
Implement parallel processing  
"""

def check_word(groups):
    word, hash_f = groups # get the group into the word and the hash
    if bcrypt.checkpw(word.encode(), hash_f.encode()): # word vs stored hash
        return word # return the cracked password
    return None

def parallel_crack(hash_f):
    # groups the words with the hash
    groups = [(word, hash_f) for word in nltk_wordlist]

    # using 6 cores since I have a 8 core cpu
    with Pool(6) as pool: # start a pool with the 6 cpu cores

        res = pool.map(check_word, groups) # run check_word for every group

    for word in res: # go through results
        if word is not None:
            return word

    return None

#Task

"""
Helper func to track time for each pw cracking  
"""

def timer(hash_f):
    start = time.time() # start time
    result = parallel_crack(hash_f) # crack the password
    duration = time.time() - start #how long it took to crack the password
    return result, duration


#Task

"""
bcrypt implementation 
"""

def main():
    path = r"C:\Users\vigt\Desktop\CyberSecurityProjects\hashing_and_passwords\Task2\shadow.txt"
    print("Loading shadow file from", path, "...")
    components = Shadow_Parse.load_shadow(path)
    print("Loaded", len(components), "entries from the shadow file.")
    print("Wordlist size:", len(nltk_wordlist), "candidate words")
    print()

    results = {}
    for entry in components:
        # show what we parsed for this user
        print("User:      ", entry.username)
        print("Algorithm: ", entry.algorithm)
        print("Workfactor:", entry.workfactor)
        print("Salt:      ", entry.salt)
        print("Hash value:", entry.hashval)

        full_hash = "$" + entry.algorithm + "$" + entry.workfactor + "$" + entry.salt + entry.hashval

        print("Cracking password for", entry.username, "... (this can take a while)")
        password, duration = timer(full_hash)

        if password is not None:
            print("  -> CRACKED:", password, "in", round(duration, 2), "seconds")
        else:
            print("  -> not found in wordlist (", round(duration, 2), "seconds )")
        print()

        results[entry.username] = {"password": password, "duration": duration}

    # final summary of everything
    print("===== Results =====")
    for user, info in results.items():
        print(user, "->", info["password"], "(", round(info["duration"], 2), "seconds )")


if __name__ == "__main__":
    main()
