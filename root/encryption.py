import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes

class Encription:
    def __init__(self, password):
        digest = hashes.Hash(hashes.SHA256())
        digest.update(password.encode())
        raw_key = digest.finalize()

        self.key = base64.urlsafe_b64encode(raw_key)
        self.f = Fernet(self.key)

    def encrypt(self, text:str):
        return self.f.encrypt(text.encode())

    def decrypt(self, token: bytes):
        return self.f.decrypt(token).decode()
        