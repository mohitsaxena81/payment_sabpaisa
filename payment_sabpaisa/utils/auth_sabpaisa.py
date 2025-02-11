import base64
from Cryptodome.Cipher import AES


class AESCipher(object):

    def __init__(self, key, iv):
        self.bs = 16
        self.key = bytes(key, "utf-8")
        self.iv = bytes(iv, 'utf-8')

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = self.iv

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = self.iv
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc)).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

        # 4w4isM1F6EOLyvqrs8/qwRNgum2ja3Wqvcb5+0K0AG4xOSY9FmmyOTXn29Z85/7qF8Xu9hxRj6nBGkvXadiVY48egykC+rLIS5jaXRIQ2G1l7hBXlXKKnmzcc4KXjQE085QSicwqQNo01v1jnD/x3sdPl+R8KVKEFVbF6C0d/NDCIO7TDb88PwmO9RR4k9gdSCWFl8z0fbS/vbtThw7Re7qDxPsMACwknbwGoxhW29r5ydYj30y+BzrzA3rmsPprHs4igrXNrR+54aFWS34NFgyUiuc6lWUCTn+ne/ZIKaqrumHNjsSdzAtluK9NqU4SosjqoFZyVlDwP3wurDjpiDbqp9kFM/d3d2x/UX6OK95qzwa71hjA79QgQi4cRNUaPYdoD6qg6T7aLSfDCssytw7IWel4pc+DYEIkPb2+y/YqbYaBE2owLygGyAhuIx/d
        # 4w4isM1F6EOLyvqrs8/qwRNgum2ja3Wqvcb5%2B0K0AG4xOSY9FmmyOTXn29Z85/7qOAS2pP0uJhpg8maxfqjWfDzfoBa3wO3xZYU6m/L4jkH05hokbaj%2BdxA6feQ8I/H8C87l2vL2KMtDwopczSfLZyxck82AbyLZeoxe%2BJsPNFJeLB0dp4wnu/R7MXjkQgJhd2sWnuZp8CA18DEbZM06tPRux37y6/tK4z7z0aKc5lyI6/shdSN7NWoVe2l3HV2l

# 4w4isM1F6EOLyvqrs8/qwRNgum2ja3Wqvcb5%2B0K0AG4xOSY9FmmyOTXn29Z85/7qOAS2pP0uJhpg8maxfqjWfDzfoBa3wO3xZYU6m/L4jkH05hokbaj%2BdxA6feQ8I/H8C87l2vL2KMtDwopczSfLZyxck82AbyLZeoxe%2BJsPNFJeLB0dp4wnu/R7MXjkQgJhd2sWnuZp8CA18DEbZM06tC1PU7qpOiAo4YR9kbbYSr8eg/iRf/GhOEpw6BfnJSEziWsIFYBZbUmvFbgiaj4ruEcc0bBKWFhbPgY5UCI1SCoId/DuL3yuguuY4rX21ckMLSIMSLW%2BO2F4EiAqghJ5Ag==
