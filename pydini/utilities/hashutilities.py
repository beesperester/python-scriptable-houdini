import hashlib

BLOCKSIZE = 1024 * 1024 * 128


def hashString(string):
    """ Hash String.

    Create unique Hash from string.

    Args:
        string string

    Returns:
        string
    """

    return hashlib.sha256(bytearray(string)).hexdigest()


def hashFile(path):
    """ Hash File.

    Create unique Hash from file.

    Args:
        string path

    Returns:
        string
    """

    hash = hashlib.sha256()

    with open(path, "rb") as f:
        fileBuffer = f.read(BLOCKSIZE)

        while len(fileBuffer) > 0:
            hash.update(fileBuffer)

            fileBuffer = f.read(BLOCKSIZE)

    return hash.hexdigest()