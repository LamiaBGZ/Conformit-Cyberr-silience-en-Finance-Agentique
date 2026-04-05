from aphb_agent import derive_key

def test_derive_key():
    key = derive_key("password", b"12345678901234567890123456789012")
    assert len(key) == 32
    