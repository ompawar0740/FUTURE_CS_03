from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

NONCE_SIZE = 12
TAG_SIZE = 16


def encrypt_file(data, key):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce + tag + ciphertext


def decrypt_file(encrypted_data, key):
    nonce = encrypted_data[:NONCE_SIZE]
    tag = encrypted_data[NONCE_SIZE:NONCE_SIZE + TAG_SIZE]
    ciphertext = encrypted_data[NONCE_SIZE + TAG_SIZE:]

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
