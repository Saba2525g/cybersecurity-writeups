import subprocess

# Extract RSA parameters from the Python 2 bytecode
cmd = [
    "python2", "-c",
    "import marshal; "
    "f=open('/home/ciel/Desktop/encrypt.pyc','rb'); "
    "f.read(8); "
    "c=marshal.load(f); "
    "print(c.co_consts[2]); "
    "print(c.co_consts[3])"
]

out = subprocess.check_output(cmd).decode().splitlines()
N = int(out[0])
e = int(out[1])

# Build a lookup table for all possible byte values
lookup = {}

for i in range(256):
    lookup[pow(i, e, N)] = i

# Download the encrypted announcement
data = subprocess.check_output([
    "curl", "-s",
    "http://127.0.0.1:3000/ftp/announcement_encrypted.md"
]).decode()

nums = [int(x) for x in data.split()]

# Decode each encrypted character
decoded = []
unknown = 0

for n in nums:
    if n in lookup:
        decoded.append(chr(lookup[n]))
    else:
        decoded.append("?")
        unknown += 1

text = "".join(decoded)

print("Characters:", len(nums))
print("Unknown:", unknown)
print("\n--- DECODED TEXT ---\n")
print(text)
