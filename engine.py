"""
CipherForge — Encryption Engine
================================
Author: Remy Ellis
Date: 2026

This file contains a custom 5-layer encryption algorithm.

PHASES:
  1. Substitution — Replace characters with different ones
  2. Transposition — Rearrange the order of characters
  3. Key-Dependent — Make output depend on a secret password
  4. Noise Injection — Add fake characters to confuse attackers
  5. Wild Card — XOR then Base64

RULES:
  - encrypt() MUST be reversible
  - decrypt(encrypt(message)) MUST return the original message
"""

import base64

DEFAULT_KEY = {
    "shift": 5,
    "block_size": 4,
    "password": "SECRET",
    "noise_interval": 3,
    "noise_chars": "~",
    "xor_password": "XORKEY",
}


def _get_key_value(key, field):
    if key is None:
        key = {}
    return key.get(field, DEFAULT_KEY[field])


def get_shift(key):
    return int(_get_key_value(key, "shift"))


def get_block_size(key):
    return int(_get_key_value(key, "block_size"))


def get_password(key):
    password = str(_get_key_value(key, "password"))
    if len(password) == 0:
        raise ValueError("password must not be empty")
    return password


def get_noise_interval(key):
    return int(_get_key_value(key, "noise_interval"))


def get_noise_chars(key):
    if key is None:
        key = {}
    # Backward compatible with older single-char name.
    noise_chars = key.get("noise_chars", key.get(
        "noise_char", DEFAULT_KEY["noise_chars"]))
    noise_chars = str(noise_chars)
    if len(noise_chars) == 0:
        raise ValueError("noise_chars must not be empty")
    return noise_chars


def get_xor_password(key):
    xor_password = str(_get_key_value(key, "xor_password"))
    if len(xor_password) == 0:
        raise ValueError("xor_password must not be empty")
    return xor_password


def caesar_shift(text, shift):
    result = ""

    for char in text:
        if 32 <= ord(char) <= 126:
            position = ord(char) - 32
            new_position = (position + shift) % 95
            result += chr(new_position + 32)
        else:
            result += char

    return result


def atbash_ascii(text):
    result = ""

    for char in text:
        if 32 <= ord(char) <= 126:
            position = ord(char) - 32
            new_position = 94 - position
            result += chr(new_position + 32)
        else:
            result += char

    return result


def phase1_encrypt(text, key=None):
    """Phase 1: Substitution using Caesar + Atbash."""
    shift = get_shift(key)
    caesar_result = caesar_shift(text, shift)
    return atbash_ascii(caesar_result)


def phase2_encrypt(text, key=None):
    """Phase 2: Transposition using block reversal."""
    block_size = get_block_size(key)

    if block_size <= 0:
        raise ValueError("block_size must be a positive integer")

    result = ""
    for i in range(0, len(text), block_size):
        block = text[i:i + block_size]
        result += block[::-1]

    return result


def phase3_encrypt(text, key=None):
    """Phase 3: Password-dependent variable shift."""
    password = get_password(key)
    result = ""

    for i, char in enumerate(text):
        if 32 <= ord(char) <= 126:
            password_char = password[i % len(password)]
            password_shift = ord(password_char) % 95
            position = ord(char) - 32
            new_position = (position + password_shift) % 95
            result += chr(new_position + 32)
        else:
            result += char

    return result


def phase4_encrypt(text, key=None):
    """Phase 4: Insert noise character every N positions."""
    interval = get_noise_interval(key)
    noise_chars = get_noise_chars(key)

    if interval <= 0:
        raise ValueError("noise_interval must be a positive integer")

    result = ""
    count = 0
    noise_count = 0

    for char in text:
        result += char
        count += 1

        if count % interval == 0:
            result += noise_chars[noise_count % len(noise_chars)]
            noise_count += 1

    return result


def phase5_encrypt(text, key=None):
    """Phase 5: Final wildcard layer using XOR encoded as Base64."""
    xor_password = get_xor_password(key)

    encrypted_bytes = bytearray()
    password_bytes = xor_password.encode("utf-8")

    for i, byte in enumerate(text.encode("utf-8")):
        key_byte = password_bytes[i % len(password_bytes)]
        encrypted_bytes.append(byte ^ key_byte)

    return base64.b64encode(encrypted_bytes).decode("ascii")


def phase1_decrypt(text, key=None):
    """Reverse Phase 1."""
    shift = get_shift(key)
    atbash_result = atbash_ascii(text)
    return caesar_shift(atbash_result, -shift)


def phase2_decrypt(text, key=None):
    """Reverse Phase 2 (self-inverse)."""
    return phase2_encrypt(text, key)


def phase3_decrypt(text, key=None):
    """Reverse Phase 3."""
    password = get_password(key)
    result = ""

    for i, char in enumerate(text):
        if 32 <= ord(char) <= 126:
            password_char = password[i % len(password)]
            password_shift = ord(password_char) % 95
            position = ord(char) - 32
            new_position = (position - password_shift) % 95
            result += chr(new_position + 32)
        else:
            result += char

    return result


def phase4_decrypt(text, key=None):
    """Reverse Phase 4 by removing known-position noise characters."""
    interval = get_noise_interval(key)
    noise_chars = get_noise_chars(key)

    if interval <= 0:
        raise ValueError("noise_interval must be a positive integer")
    if len(noise_chars) == 0:
        raise ValueError("noise_chars must not be empty")

    result = ""
    real_count = 0
    i = 0

    while i < len(text):
        result += text[i]
        real_count += 1
        i += 1

        if real_count % interval == 0 and i < len(text):
            i += 1  # skip one noise character

    return result


def phase5_decrypt(text, key=None):
    """Reverse Phase 5."""
    xor_password = get_xor_password(key)

    encrypted_bytes = base64.b64decode(text.encode("ascii"))
    result = bytearray()
    password_bytes = xor_password.encode("utf-8")

    for i, byte in enumerate(encrypted_bytes):
        key_byte = password_bytes[i % len(password_bytes)]
        result.append(byte ^ key_byte)

    return bytes(result).decode("utf-8")


def encrypt(text, key=None):
    """CipherForge Master Encryption — applies all 5 phases."""
    result = phase1_encrypt(text, key)
    result = phase2_encrypt(result, key)
    result = phase3_encrypt(result, key)
    result = phase4_encrypt(result, key)
    result = phase5_encrypt(result, key)
    return result


def decrypt(text, key=None):
    """CipherForge Master Decryption — reverses all 5 phases."""
    result = phase5_decrypt(text, key)
    result = phase4_decrypt(result, key)
    result = phase3_decrypt(result, key)
    result = phase2_decrypt(result, key)
    result = phase1_decrypt(result, key)
    return result
