from pathlib import Path
from apbh_agent import derive_key, encrypt_file, decrypt_file


def test_derive_key():
    key = derive_key("password", b"12345678901234567890123456789012")
    assert len(key) == 32


def test_encrypt_decrypt():
    test_file = Path("test_data/test_unit.txt")

    # créer fichier test
    test_file.write_text("secret data")

    password = "test123"

    # chiffrement
    encrypt_file(test_file, password)

    encrypted_file = Path("test_data/test_unit.txt.aphb")
    assert encrypted_file.exists()

    # déchiffrement
    decrypt_file(encrypted_file, password)

    assert test_file.exists()
    assert test_file.read_text() == "secret data"
