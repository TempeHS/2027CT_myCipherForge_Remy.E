ciphertext = "Jrypbzr gb PvcuresBefr!'"
known_word = "welcome"


def caesar_shift(text, shift):
    result = ""

    for char in text:
        if "a" <= char <= "z":
            start = ord("a")
            result += chr((ord(char) - start + shift) % 26 + start)
        elif "A" <= char <= "Z":
            start = ord("A")
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char

    return result


for shift in range(26):
    decoded = caesar_shift(ciphertext, shift)

    if known_word in decoded.lower():
        print(f"Match found with shift {shift}: {decoded}")
    else:
        print(f"Shift {shift}: {decoded}")
