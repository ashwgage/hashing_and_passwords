import hashlib
import time
import matplotlib.pyplot as plt


# convert the string into bytes, hash the bytes, return in hex
def sha256_hash(input_string):
    string_bytes = input_string.encode()
    return hashlib.sha256(string_bytes).hexdigest()

def task_1a():
    pass

# requirement says your two inputs need to differ by exactly one bit. 
# The professor’s notes suggest generating a string and flipping a bit in it
def flip_bit(data, byte_index, bit_index):
    value = bytearray(data)  # convert bytes into a mutable byte array
    flipped_bit = value[byte_index] ^ (1 << bit_index)  # flip the selected bit using XOR
    value[byte_index] = flipped_bit
    res = bytes(value)  # convert the result back to bytes
    return res

def hamming_distance(s1, s2):
    count = 0
    # Loop through every index from 0 to the length of the string
    for i in range(len(s1)):
        # Compare characters at the exact same position
        if s1[i] != s2[i]:
            count += 1
    return count


def task_1b():
    original = b"hello"

    modified1 = flip_bit(original, 0, 0)
    modified2 = flip_bit(original, 1, 2)
    modified3 = flip_bit(original, 3, 5)

    print(f"Original input: {original}")
    print(f"Original SHA256: {hashlib.sha256(original).hexdigest()}")

    print(f"\nModified 1: {modified1}")
    print(f"SHA256: {hashlib.sha256(modified1).hexdigest()}")
    print(f"Hamming distance: {hamming_distance(original, modified1)}")

    print(f"\nModified 2: {modified2}")
    print(f"SHA256: {hashlib.sha256(modified2).hexdigest()}")
    print(f"Hamming distance: {hamming_distance(original, modified2)}")

    print(f"\nModified 3: {modified3}")
    print(f"SHA256: {hashlib.sha256(modified3).hexdigest()}")
    print(f"Hamming distance: {hamming_distance(original, modified3)}")


# Take the first (bits / 4) characters of the hash string
# Convert that substring to an integer
# Create a bitmask of 'bits' number of 1s
# Perform bitwise AND
# Return the result
def truncate_hash(hash_string, bits):
    # take enough hex characters from the front
    hex_chars = (bits + 3) // 4
    val = hash_string[:hex_chars]

    # convert the hex substring into an integer
    val = int(val, 16)

    # remove any extra bits from the last hex character
    extra_bits = (hex_chars * 4) - bits
    val = val >> extra_bits

    return val

# create an empty dictionary, generate different inputs, calculate each truncated hash, 
# and check whether that hash has already been seen. If it has, you found a collision
def find_collision(bits):
    seen = {}

    # keep track of how many inputs we have tried
    attempts = 0

    start_time = time.perf_counter()

    while True:
        input_string = str(attempts)
        hash_string = sha256_hash(input_string)
        truncated = truncate_hash(hash_string, bits)

        # check whether this truncated hash is already in seen
        if truncated in seen:
            end_time = time.perf_counter() - start_time

            return seen[truncated], input_string, attempts + 1, end_time
        else:
            seen[truncated] = input_string
 
        attempts += 1
        

def task_1c():
    bits_list = []
    attempts_list = []
    time_list = []

    for bits in range(8, 51, 2):
        input1, input2, attempts, elapsed = find_collision(bits)

        bits_list.append(bits)
        attempts_list.append(attempts)
        time_list.append(elapsed)

        hash1 = sha256_hash(input1)
        hash2 = sha256_hash(input2)

        truncated1 = truncate_hash(hash1, bits)
        truncated2 = truncate_hash(hash2, bits)

        print(f"\nDigest size: {bits} bits")
        print(f"Input 1: {input1}")
        print(f"Input 2: {input2}")
        print(f"Truncated hash 1: {truncated1}")
        print(f"Truncated hash 2: {truncated2}")
        print(f"Attempts: {attempts}")
        print(f"Time: {elapsed:.6f} seconds")


def main():
    task_1a()
    task_1b()
    task_1c()


if __name__ == "__main__":
    main()
