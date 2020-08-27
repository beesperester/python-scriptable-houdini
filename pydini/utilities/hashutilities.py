import hashlib

BLOCKSIZE = 1024 * 1024 * 128

def hashString(string):
    return hashlib.sha256(bytearray(string)).hexdigest()

def hashFile(path):
    hash = hashlib.sha256()

    with open(path, "rb") as f:
        fileBuffer = f.read(BLOCKSIZE)

        while len(fileBuffer) > 0:
            hash.update(fileBuffer)

            fileBuffer = f.read(BLOCKSIZE)

    return hash.hexdigest()