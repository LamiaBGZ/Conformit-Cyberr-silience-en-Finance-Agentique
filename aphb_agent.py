#!/usr/bin/env python3
"""
AP-HB Encryption Agent v1.0
Chiffrement AES-256-GCM automatique de répertoires sensibles
Licence: MIT — Open Source
"""

import os, json, logging, argparse
from pathlib import Path
from datetime import datetime
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64, getpass

logging.basicConfig(
    filename='aphb_encryption_agent.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive AES-256 key from password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256 bits
        salt=salt,
        iterations=100_000,
    )
    return kdf.derive(password.encode())

def encrypt_file(path: Path, password: str) -> dict:
    """Encrypt a single file with AES-256-GCM."""
    salt = os.urandom(32)   # Random salt
    iv   = os.urandom(12)   # Random IV for GCM
    key  = derive_key(password, salt)
    aesgcm = AESGCM(key)
    data = path.read_bytes()
    ciphertext = aesgcm.encrypt(iv, data, None)
    out_path = path.with_suffix(path.suffix + '.aphb')
    # Store: salt(32) + iv(12) + ciphertext
    out_path.write_bytes(salt + iv + ciphertext)
    os.remove(path)  # Secure delete original
    logging.info(f'ENCRYPTED: {path} -> {out_path}')
    return {'file': str(path), 'status': 'encrypted', 'ts': datetime.utcnow().isoformat()}

def decrypt_file(path: Path, password: str) -> dict:
    """Decrypt a .aphb encrypted file."""
    raw = path.read_bytes()
    salt, iv, ciphertext = raw[:32], raw[32:44], raw[44:]
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    data = aesgcm.decrypt(iv, ciphertext, None)
    out_path = path.with_suffix('')  # Remove .aphb
    out_path.write_bytes(data)
    os.remove(path)
    logging.info(f'DECRYPTED: {path} -> {out_path}')
    return {'file': str(path), 'status': 'decrypted', 'ts': datetime.utcnow().isoformat()}

def process_directory(directory: str, password: str, mode: str):
    """Recursively encrypt or decrypt all files in directory."""
    target = Path(directory)
    results = []
    for f in target.rglob('*'):
        if not f.is_file(): continue
        try:
            if mode == 'encrypt' and not str(f).endswith('.aphb'):
                results.append(encrypt_file(f, password))
            elif mode == 'decrypt' and str(f).endswith('.aphb'):
                results.append(decrypt_file(f, password))
        except Exception as e:
            logging.error(f'ERROR {f}: {e}')
    report = {'directory': directory, 'mode': mode, 'count': len(results), 'files': results}
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AP-HB Encryption Agent')
    parser.add_argument('directory', help='Target directory path')
    parser.add_argument('--mode', choices=['encrypt','decrypt'], default='encrypt')
    args = parser.parse_args()
    pwd = getpass.getpass('Passphrase AP-HB: ')
    process_directory(args.directory, pwd, args.mode)
