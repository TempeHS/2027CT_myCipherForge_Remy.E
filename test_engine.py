"""Test suite for CipherForge encryption algorithm.

Run with: python test_engine.py
"""

from engine import (
    phase1_encrypt, phase1_decrypt,
    phase2_encrypt, phase2_decrypt,
    phase3_encrypt, phase3_decrypt,
    phase4_encrypt, phase4_decrypt,
    phase5_encrypt, phase5_decrypt,
    encrypt, decrypt
)


def test_phase1():
    """Test Phase 1: Caesar shift."""
    key = {"shift": 5}

    # Test encryption
    original = "Hello"
    encrypted = phase1_encrypt(original, key)
    assert encrypted != original, "Phase 1 should change the text"

    # Test decryption reverses encryption
    decrypted = phase1_decrypt(encrypted, key)
    assert decrypted == original, f"Phase 1 decrypt failed: got {decrypted}"

    print("✅ Phase 1 tests passed")


def test_phase2():
    """Test Phase 2: Block reversal."""
    key = {"block_size": 4}

    original = "ABCDEFGH"
    encrypted = phase2_encrypt(original, key)

    # Block reversal should rearrange characters
    assert encrypted != original, "Phase 2 should change the text"

    # Decryption should restore original
    decrypted = phase2_decrypt(encrypted, key)
    assert decrypted == original, f"Phase 2 decrypt failed: got {decrypted}"

    print("✅ Phase 2 tests passed")


def test_phase3():
    """Test Phase 3: Password-based variable shift."""
    key = {"password": "SECRET"}

    original = "Test message"
    encrypted = phase3_encrypt(original, key)

    assert encrypted != original, "Phase 3 should change the text"

    decrypted = phase3_decrypt(encrypted, key)
    assert decrypted == original, f"Phase 3 decrypt failed: got {decrypted}"

    print("✅ Phase 3 tests passed")


def test_phase4():
    """Test Phase 4: Noise injection."""
    key = {"noise_interval": 3, "noise_char": "~"}

    original = "ABCDEF"
    encrypted = phase4_encrypt(original, key)

    # Noise injection should make text longer
    assert len(encrypted) > len(original), "Phase 4 should add characters"

    decrypted = phase4_decrypt(encrypted, key)
    assert decrypted == original, f"Phase 4 decrypt failed: got {decrypted}"

    print("✅ Phase 4 tests passed")


def test_phase5():
    """Test Phase 5: Your wild card."""
    key = {}  # Phase 5 may or may not use key

    original = "Wild card test"
    encrypted = phase5_encrypt(original, key)

    decrypted = phase5_decrypt(encrypted, key)
    assert decrypted == original, f"Phase 5 decrypt failed: got {decrypted}"

    print("✅ Phase 5 tests passed")


def test_full_pipeline():
    """Test all 5 phases combined."""
    key = {
        "shift": 7,
        "block_size": 5,
        "password": "TESTKEY",
        "noise_interval": 4,
        "noise_char": "$"
    }

    test_messages = [
        "Hello World!",
        "CipherForge 2026",
        "The quick brown fox",
        "abc123!@#",
        "A",
        "AB"
    ]

    for message in test_messages:
        encrypted = encrypt(message, key)
        decrypted = decrypt(encrypted, key)
        assert decrypted == message, f"Pipeline failed for '{message}': got '{decrypted}'"

    print("✅ Full pipeline tests passed")


def test_different_keys():
    """Test that different keys produce different results."""
    key1 = {"shift": 5, "block_size": 4, "password": "KEY1",
            "noise_interval": 3, "noise_char": "~"}
    key2 = {"shift": 10, "block_size": 6, "password": "KEY2",
            "noise_interval": 4, "noise_char": "#"}

    message = "Same message"

    encrypted1 = encrypt(message, key1)
    encrypted2 = encrypt(message, key2)

    assert encrypted1 != encrypted2, "Different keys should produce different ciphertext"

    # But each should still decrypt correctly with its own key
    assert decrypt(encrypted1, key1) == message
    assert decrypt(encrypted2, key2) == message

    print("✅ Different keys test passed")


def run_all_tests():
    """Run all test functions."""
    print("="*60)
    print("CIPHERFORGE TEST SUITE")
    print("="*60)

    test_phase1()
    test_phase2()
    test_phase3()
    test_phase4()
    test_phase5()
    test_full_pipeline()
    test_different_keys()

    print("="*60)
    print("🎉 ALL TESTS PASSED!")
    print("="*60)


if __name__ == "__main__":
    run_all_tests()
