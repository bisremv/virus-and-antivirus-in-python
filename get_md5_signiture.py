import hashlib

def calculate_md5(file_path):
    """Calculate MD5 hash of a file."""
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()



# Example usage
if __name__ == "__main__":
    print(calculate_md5(r"C:\Users\bisreMV\Documents\security\file_Infection_virus\target_folder\infector_virus.exe"))