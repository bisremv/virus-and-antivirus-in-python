import os
import hashlib

def calculate_md5(file_path):
    """Calculate MD5 hash of a file."""
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()

def scan_directory(directory_path, known_virus_hashes):
    """Scan a directory and its subdirectories for potentially infected files."""
    infected_files = []
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if is_file_infected(file_path, known_virus_hashes):
                infected_files.append(file_path)
    return infected_files

def is_file_infected(file_path, known_virus_hashes):
    """Check if file is infected based on its MD5 hash."""
    try:
        with open(file_path, "rb") as f:
            file_hash = calculate_md5(file_path)
            if file_hash in known_virus_hashes:
                return True
    except Exception as e:
        print(f"Error scanning file {file_path}: {e}")
    return False

def handle_infected_files(infected_files):
    """Handle potentially infected files."""
    for file_path in infected_files:
        print(f"Potentially infected file found: {file_path}")
        action = input("Do you want to delete (D) or ignore (I) this file? ").strip().lower()
        if action == 'd':
            try:
                os.remove(file_path)
                print(f"File {file_path} deleted.")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
        elif action == 'i':
            print(f"File {file_path} ignored.")
        else:
            print("Invalid option. Please choose 'D' to delete or 'I' to ignore.")

# Example usage
if __name__ == "__main__":
    current_directory = os.getcwd()
    known_virus_hashes = ["7a6e4fd7532a77cba60d511521a5eb94","7a6e4fd7532a77cba60d511521a5eb94"]
    infected_files = scan_directory(current_directory, known_virus_hashes)
    if infected_files:
        handle_infected_files(infected_files)
    else:
        print("No infected files found.")
