import hashlib
import base64
import os
from Crypto.Cipher import AES

def encrypt_aes(word, key):
  

    word_bytes = word.encode('utf-8')
    iv = os.urandom(16)  # Menghasilkan IV acak dengan panjang 16 byte
    encryption_key = hashlib.md5(key.encode()).digest()

    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    padding = AES.block_size - len(word_bytes) % AES.block_size
    word_bytes += bytes([padding]) * padding
    encrypted_data = iv + cipher.encrypt(word_bytes)
    
    return encrypted_data

    
def decrypt_aes(ciphertext, key):
   
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]

    encryption_key = hashlib.md5(key.encode()).digest()

    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(ciphertext)

    padding = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding]
    string_data = decrypted_data.decode('utf-8')

    return string_data
    


print (decrypt_aes(encrypt_aes('testimoni', 'kunci_rahasia'), 'kunci_rahasia'))
