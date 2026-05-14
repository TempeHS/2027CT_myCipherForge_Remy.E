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

    if shift is None:
        raise ValueError("CIPHER_SHIFT is missing from .env")
    if block_size is None:
        raise ValueError("CIPHER_TRANSPOSE_BLOCK_SIZE is missing from .env")

    return {
        "shift": int(shift),
        "block_size": int(block_size)
    }


def get_shift(key):
    if key is None:
        key = load_key()

    return key["shift"]


def get_block_size(key):
    if key is None:
        key = load_key()

    return key["block_size"]


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
    try:
        # Get block size from key (default to 4 if not specified)
        block_size = get_block_size(key)
        
        result = ""
        
        # Process text in chunks of block_size
        for i in range(0, len(text), block_size):
            # Extract this block (might be shorter at the end)
            block = text[i:i + block_size]
            # Reverse the block and add to result
            result += block[::-1]
        
        return result
    except ValueError:
        return print("Key must be a positive integer for block size. Check .env or pass a key dictionary.")

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
    
    # TODO: Phase 3 — Key-Dependent
    # result = phase3_encrypt(result, key)
    
    # TODO: Phase 4 — Noise Injection
    # result = phase4_encrypt(result, key)
    
    # TODO: Phase 5 — Wild Card
    # result = phase5_encrypt(result, key)
    
    return result


def decrypt(text, key=None):
    """
    CipherForge Master Decryption - Reverses all implemented phases.

    Args:
        text: The encrypted string
        key: Dictionary with settings for all phases

    Returns:
        The decrypted original string
    """
    # Phase 2: Reverse transposition
    result = phase2_decrypt(text, key)

    # Phase 1: Reverse substitution
    result = phase1_decrypt(result, key)

    return result
