
from collections import Counter

def get_ic(ciphertext, d):
    total = 0

    # split ciphertext into d groups
    groups = []
    for i in range(d):
        groups.append(ciphertext[i::d])

    for group in groups:
        # get frequency table of each letter
        lst = Counter(group)

        # iterate through dict
        freq_total = 0
        for key, value in lst.items():
            freq_total += value*(value-1)
        
        print(lst)
        # compute IC
        if len(group) > 1:
            total +=  freq_total / (len(group)*(len(group)-1))

    return total / d

def decrypt(ciphertext, key):
    decrypted_text = []
    key = key.upper()
    key_length = len(key)

    for i, char in enumerate(ciphertext):
        if char.isalpha():  # Ignore non-alphabetic characters
            key_letter = key[i % 4]  # Cycle through key
            key_shift = ord(key_letter) - ord('A')  # Convert key letter to shift value

            decrypted_letter = chr(((ord(char) - ord('A') - key_shift) % 26) + ord('A'))
            decrypted_text.append(decrypted_letter)
        else:
            decrypted_text.append(char)  # Preserve spaces/punctuation

    return "".join(decrypted_text)


ciphertext = "BEZRLEKVUPVKHQWZFPVZMHDJMSHNHCVKHQWZFPVZMHDJMSHRZPRWPTVUHXLKPLVKAPDXXZIWHZOZLSQVLDLKPLVKAPHGHNKFYMHCBPIZMHDJMSHVIZFYHQLEVCHUNWLKY"
key_lens = [4]

for i in key_lens:
    print(f"IC length {i}: {get_ic(ciphertext, i)}")

print(decrypt(ciphertext, "DLRG"))
