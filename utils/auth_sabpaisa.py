# import base64
# from Cryptodome.Cipher import AES


# class AESCipher(object):

#     def __init__(self, key, iv):
#         self.bs = 16
#         self.key = bytes(key, "utf-8")
#         self.iv = bytes(iv, 'utf-8')

#     def encrypt(self, raw):
#         raw = self._pad(raw)
#         iv = self.iv

#         cipher = AES.new(self.key, AES.MODE_CBC, iv)
#         return base64.b64encode(cipher.encrypt(raw.encode()))

#     def decrypt(self, enc):
#         enc = base64.b64decode(enc)
#         iv = self.iv
#         cipher = AES.new(self.key, AES.MODE_CBC, iv)
#         return self._unpad(cipher.decrypt(enc)).decode('utf-8')

#     def _pad(self, s):
#         return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

#     @staticmethod
#     def _unpad(s):
#         return s[:-ord(s[len(s) - 1:])]

        # 4w4isM1F6EOLyvqrs8/qwRNgum2ja3Wqvcb5+0K0AG4xOSY9FmmyOTXn29Z85/7qF8Xu9hxRj6nBGkvXadiVY48egykC+rLIS5jaXRIQ2G1l7hBXlXKKnmzcc4KXjQE085QSicwqQNo01v1jnD/x3sdPl+R8KVKEFVbF6C0d/NDCIO7TDb88PwmO9RR4k9gdSCWFl8z0fbS/vbtThw7Re7qDxPsMACwknbwGoxhW29r5ydYj30y+BzrzA3rmsPprHs4igrXNrR+54aFWS34NFgyUiuc6lWUCTn+ne/ZIKaqrumHNjsSdzAtluK9NqU4SosjqoFZyVlDwP3wurDjpiDbqp9kFM/d3d2x/UX6OK95qzwa71hjA79QgQi4cRNUaPYdoD6qg6T7aLSfDCssytw7IWel4pc+DYEIkPb2+y/YqbYaBE2owLygGyAhuIx/d
        # 4w4isM1F6EOLyvqrs8/qwRNgum2ja3Wqvcb5%2B0K0AG4xOSY9FmmyOTXn29Z85/7qOAS2pP0uJhpg8maxfqjWfDzfoBa3wO3xZYU6m/L4jkH05hokbaj%2BdxA6feQ8I/H8C87l2vL2KMtDwopczSfLZyxck82AbyLZeoxe%2BJsPNFJeLB0dp4wnu/R7MXjkQgJhd2sWnuZp8CA18DEbZM06tPRux37y6/tK4z7z0aKc5lyI6/shdSN7NWoVe2l3HV2l

# 4w4isM1F6EOLyvqrs8/qwRNgum2ja3Wqvcb5%2B0K0AG4xOSY9FmmyOTXn29Z85/7qOAS2pP0uJhpg8maxfqjWfDzfoBa3wO3xZYU6m/L4jkH05hokbaj%2BdxA6feQ8I/H8C87l2vL2KMtDwopczSfLZyxck82AbyLZeoxe%2BJsPNFJeLB0dp4wnu/R7MXjkQgJhd2sWnuZp8CA18DEbZM06tC1PU7qpOiAo4YR9kbbYSr8eg/iRf/GhOEpw6BfnJSEziWsIFYBZbUmvFbgiaj4ruEcc0bBKWFhbPgY5UCI1SCoId/DuL3yuguuY4rX21ckMLSIMSLW%2BO2F4EiAqghJ5Ag==


import base64
import os
import hmac
import hashlib
from Crypto.Cipher import AES

class AESCipher(object):
    IV_SIZE = 12  
    TAG_SIZE = 16  
    HMAC_LENGTH = 48  

    def __init__(self, auth_key, auth_iv):
        
        auth_key = auth_key.strip()
        auth_iv = auth_iv.strip()

        self.auth_key = base64.b64decode(auth_key)
        self.auth_iv = base64.b64decode(auth_iv)

    @staticmethod
    def bytes_to_hex(b):
        return b.hex().upper()

    @staticmethod
    def hex_to_bytes(h):
        return bytes.fromhex(h)

    def encrypt(self, plaintext):
        iv = os.urandom(self.IV_SIZE)
        cipher = AES.new(self.auth_key, AES.MODE_GCM, nonce=iv, mac_len=self.TAG_SIZE)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))

        encrypted_message = iv + ciphertext + tag
        hmac_calculated = hmac.new(self.auth_iv, encrypted_message, hashlib.sha384).digest()
        final_message = hmac_calculated + encrypted_message

        return self.bytes_to_hex(final_message)

    def decrypt(self, hex_ciphertext):
        full_message = self.hex_to_bytes(hex_ciphertext)

        if len(full_message) < self.HMAC_LENGTH + self.IV_SIZE + self.TAG_SIZE:
            raise ValueError("Invalid ciphertext length")

        hmac_received = full_message[:self.HMAC_LENGTH]
        encrypted_data = full_message[self.HMAC_LENGTH:]

        hmac_calculated = hmac.new(self.auth_iv, encrypted_data, hashlib.sha384).digest()
        if not hmac.compare_digest(hmac_received, hmac_calculated):
            raise ValueError("HMAC validation failed. Data may be tampered!")

        iv = encrypted_data[:self.IV_SIZE]
        ciphertext_with_tag = encrypted_data[self.IV_SIZE:]

        ciphertext = ciphertext_with_tag[:-self.TAG_SIZE]
        tag = ciphertext_with_tag[-self.TAG_SIZE:]

        cipher = AES.new(self.auth_key, AES.MODE_GCM, nonce=iv, mac_len=self.TAG_SIZE)
        plaintext_bytes = cipher.decrypt_and_verify(ciphertext, tag)

        return plaintext_bytes.decode('utf-8')
