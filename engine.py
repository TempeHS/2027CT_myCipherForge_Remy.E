"""
CipherForge — Encryption Engine
================================
Author: Remy Ellis
Date: 2026

This file contains my custom 5-layer encryption algorithm.

PHASES:
  1. Substitution — Replace characters with different ones
  2. Transposition — Rearrange the order of characters  
  3. Key-Dependent — Make output depend on a secret password
  4. Noise Injection — Add fake characters to confuse attackers
  5. Wild Card — My unique invention!

RULES:
  - encrypt() MUST be reversible
  - decrypt(encrypt(message)) MUST return the original message
"""

import os

from dotenv import load_dotenv

load_dotenv()

def load_key():
    shift = os.getenv("CIPHER_SHIFT")
    block_size = os.getenv("CIPHER_TRANSPOSE_BLOCK_SIZE")
    password = os.getenv("CIPHER_PASSWORD")

    if shift is None:
        raise ValueError("CIPHER_SHIFT is missing from .env")
    if block_size is None:
        raise ValueError("CIPHER_TRANSPOSE_BLOCK_SIZE is missing from .env")
    if password is None:
        raise ValueError("CIPHER_PASSWORD is missing from .env")

    return {
        "shift": int(shift),
        "block_size": int(block_size),
        "password": password
    }


def get_shift(key):
    if key is None:
        key = load_key()

    return key["shift"]


def get_block_size(key):
    if key is None:
        key = load_key()

    return key["block_size"]


def get_password(key):
    if key is None:
        key = load_key()

    return key["password"]


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
    """
    Phase 1: Substitution — Shift every character by a fixed amount.
    
    This layer changes WHAT each character is (its identity).
    
    Args:
        text: The plaintext string to encrypt
        key: Dictionary containing encryption settings
        
    Returns:
        The encrypted string with all characters shifted
    """
    # Caesar
    # Get the shift amount from the key loaded from .env.
    shift = get_shift(key)

    caesar_result = caesar_shift(text, shift)
    result = atbash_ascii(caesar_result)

    return result

def phase2_encrypt(text, key=None):
    """
    Phase 2: Transposition — Rearrange character positions.
    
    Uses block reversal: split into blocks and reverse each one.
    This layer changes WHERE each character is (its position).
    
    Args:
        text: The string to transform (already Phase 1 encrypted)
        key: Dictionary containing encryption settings
        
    Returns:
        The transposed string with characters rearranged
    """
    # Get block size from key loaded from .env.
    block_size = get_block_size(key)

    if block_size <= 0:
        raise ValueError("CIPHER_TRANSPOSE_BLOCK_SIZE must be a positive integer")

    result = ""

    # Process text in chunks of block_size
    for i in range(0, len(text), block_size):
        # Extract this block (might be shorter at the end)
        block = text[i:i + block_size]
        # Reverse the block and add to result
        result += block[::-1]

    return result

def phase3_encrypt(text, key=None):
    """
    Phase 3: Password-Dependent — Variable shifts based on password.
    
    Each character is shifted by a different amount determined by
    the corresponding character in the repeating password.
    This destroys frequency patterns!
    
    Args:
        text: The string to transform (already Phase 1+2 encrypted)
        key: Dictionary containing encryption settings
        
    Returns:
        The password-encrypted string
    """
    # Get password from key loaded from .env.
    password = get_password(key)
    
    result = ""
    
    for i, char in enumerate(text):
        if 32 <= ord(char) <= 126:
            # Get the password character for this position (cycling)
            password_char = password[i % len(password)]
            # Calculate shift from password character
            password_shift = ord(password_char) % 95
            
            # Apply the shift (same math as Phase 1)
            position = ord(char) - 32
            new_position = (position + password_shift) % 95
            result += chr(new_position + 32)
        else:
            result += char
    
    return result

def phase1_decrypt(text, key=None):
    """
    Phase 1: Reverse the substitution.
    
    Decryption shifts in the OPPOSITE direction (subtracts instead of adds).
    
    Args:
        text: The encrypted string
        key: Dictionary containing the same encryption settings
        
    Returns:
        The decrypted (original) string
    """
    shift = get_shift(key)

    atbash_result = atbash_ascii(text)
    result = caesar_shift(atbash_result, -shift)

    return result

def phase2_decrypt(text, key=None):
    """
    Phase 2: Reverse the transposition.
    
    For block reversal, decryption is the same as encryption!
    Reversing a reversed block returns the original.
    
    Args:
        text: The transposed string
        key: Dictionary containing the same encryption settings
        
    Returns:
        The un-transposed string
    """
    # Block reversal is self-inverting: encrypt == decrypt
    # Reverse twice = original!
    return phase2_encrypt(text, key)

def phase3_decrypt(text, key=None):
    """
    Phase 3: Reverse the password-dependent encryption.
    
    CRITICAL: Must use the SAME password that was used for encryption!
    Wrong password = garbage output.
    
    Args:
        text: The encrypted string
        key: Dictionary with the SAME password used for encryption
        
    Returns:
        The decrypted string (if password is correct)
    """
    password = get_password(key)
    
    result = ""
    
    for i, char in enumerate(text):
        if 32 <= ord(char) <= 126:
            # Get same password character for this position
            password_char = password[i % len(password)]
            password_shift = ord(password_char) % 95
            
            # SUBTRACT the shift to reverse encryption
            position = ord(char) - 32
            new_position = (position - password_shift) % 95
            result += chr(new_position + 32)
        else:
            result += char
    
    return result

def encrypt(text, key=None):
    """
    CipherForge Master Encryption — Applies all 5 phases.
    
    Currently implemented: Phase 1 only
    Coming soon: Phases 2-5
    
    Args:
        text: The plaintext to encrypt
        key: Dictionary with settings for all phases
        
    Returns:
        Fully encrypted string
    """
    # Phase 1: Substitution
    result = phase1_encrypt(text, key)
    
    # Phase 2: Transposition
    result = phase2_encrypt(result, key)
    
    # Phase 3: Key-Dependent
    result = phase3_encrypt(result, key)
    
    # TODO: Phase 4 — Noise Injection
    # result = phase4_encrypt(result, key)
    
    # TODO: Phase 5 — Wild Card
    # result = phase5_encrypt(result, key)
    
    return result

def decrypt(text, key):
    """
    CipherForge Master Decryption — Reverses all 5 phases.
    
    CRITICAL: Phases reversed in OPPOSITE order!
    Encrypt: 1 → 2 → 3 → 4 → 5
    Decrypt: 5 → 4 → 3 → 2 → 1
    """
    result = text
    
    # TODO: Phase 5 — Reverse Wild Card (first!)
    # result = phase5_decrypt(result, key)
    
    # TODO: Phase 4 — Reverse Noise Injection
    # result = phase4_decrypt(result, key)
    
    # Phase 3: Reverse Password-Dependent
    result = phase3_decrypt(result, key)
    
    # Phase 2: Reverse Transposition
    result = phase2_decrypt(result, key)
    
    # Phase 1: Reverse Substitution (last!)
    result = phase1_decrypt(result, key)
    
    return result
