#!/usr/bin/env python3
"""
AP-BH Encryption Agent v1.1
Chiffrement AES-256-GCM automatique de répertoires sensibles
Licence: MIT — Open Source
"""

import argparse
import getpass
import json
import logging
import os
from datetime import datetime
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


SALT_SIZE = 32
IV_SIZE = 12
KEY_SIZE = 32
PBKDF2_ITERATIONS = 100_000
ENCRYPTED_EXTENSION = ".aphb"
LOG_FILE = "apbh_encryption_agent.log"


def setup_logging() -> None:
    """Configure logging for the agent."""
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive an AES-256 key from a password using PBKDF2-HMAC-SHA256."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt_file(path: Path, password: str) -> dict:
    """Encrypt a single file with AES-256-GCM."""
    if path.suffix == ENCRYPTED_EXTENSION:
        raise ValueError(f"File is already encrypted: {path}")

    salt = os.urandom(SALT_SIZE)
    iv = os.urandom(IV_SIZE)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    data = path.read_bytes()
    ciphertext = aesgcm.encrypt(iv, data, None)

    out_path = path.with_name(path.name + ENCRYPTED_EXTENSION)
    out_path.write_bytes(salt + iv + ciphertext)

    if not out_path.exists() or out_path.stat().st_size == 0:
        raise IOError(f"Encrypted file was not written correctly: {out_path}")

    path.unlink()

    logging.info("ENCRYPTED: %s -> %s", path, out_path)
    return {
        "file": str(path),
        "output": str(out_path),
        "status": "encrypted",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


def decrypt_file(path: Path, password: str) -> dict:
    """Decrypt a single .aphb encrypted file."""
    if path.suffix != ENCRYPTED_EXTENSION:
        raise ValueError(f"File is not an encrypted .aphb file: {path}")

    raw = path.read_bytes()
    minimum_size = SALT_SIZE + IV_SIZE + 16  # GCM tag included in ciphertext payload

    if len(raw) < minimum_size:
        raise ValueError(f"Encrypted file is too short or corrupted: {path}")

    salt = raw[:SALT_SIZE]
    iv = raw[SALT_SIZE:SALT_SIZE + IV_SIZE]
    ciphertext = raw[SALT_SIZE + IV_SIZE:]

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    try:
        data = aesgcm.decrypt(iv, ciphertext, None)
    except InvalidTag as exc:
        raise ValueError(f"Authentication failed for file: {path}") from exc

    out_path = path.with_suffix("")

    out_path.write_bytes(data)

    if not out_path.exists():
        raise IOError(f"Decrypted file was not written correctly: {out_path}")

    path.unlink()

    logging.info("DECRYPTED: %s -> %s", path, out_path)
    return {
        "file": str(path),
        "output": str(out_path),
        "status": "decrypted",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


def process_directory(directory: str, password: str, mode: str) -> dict:
    """Recursively encrypt or decrypt all eligible files in a directory."""
    target = Path(directory)

    if not target.exists():
        raise FileNotFoundError(f"Directory does not exist: {directory}")

    if not target.is_dir():
        raise NotADirectoryError(f"Provided path is not a directory: {directory}")

    logging.info("START | mode=%s | directory=%s", mode, target)

    results = []
    errors = []

    for file_path in target.rglob("*"):
        if not file_path.is_file():
            continue

        try:
            if mode == "encrypt" and file_path.suffix != ENCRYPTED_EXTENSION:
                results.append(encrypt_file(file_path, password))
            elif mode == "decrypt" and file_path.suffix == ENCRYPTED_EXTENSION:
                results.append(decrypt_file(file_path, password))
        except Exception as exc:
            logging.error("ERROR: %s | %s", file_path, exc)
            errors.append(
                {
                    "file": str(file_path),
                    "error": str(exc),
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                }
            )

    report = {
        "directory": str(target.resolve()),
        "mode": mode,
        "processed_count": len(results),
        "error_count": len(errors),
        "files": results,
        "errors": errors,
    }

    logging.info(
        "END | mode=%s | directory=%s | processed=%s | errors=%s",
        mode,
        target,
        len(results),
        len(errors),
    )

    return report


def main() -> None:
    """CLI entry point."""
    setup_logging()

    parser = argparse.ArgumentParser(description="AP-BH Encryption Agent")
    parser.add_argument("directory", help="Target directory path")
    parser.add_argument(
        "--mode",
        choices=["encrypt", "decrypt"],
        default="encrypt",
        help="Operation mode: encrypt or decrypt",
    )

    args = parser.parse_args()
    password = getpass.getpass("Passphrase AP-BH: ")

    if not password.strip():
        raise ValueError("Passphrase cannot be empty.")

    report = process_directory(args.directory, password, args.mode)
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
