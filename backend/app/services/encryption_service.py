from cryptography.fernet import Fernet
from backend.app.core.config import settings

class EncryptionService:
    def __init__(self):
        # Ensure a 32-byte urlsafe base64 key
        try:
            self.fernet = Fernet(settings.ENCRYPTION_SECRET_KEY.encode())
        except Exception:
            # Fallback for dev if invalid key provided
            key = Fernet.generate_key()
            self.fernet = Fernet(key)

    def encrypt_bytes(self, data: bytes) -> bytes:
        return self.fernet.encrypt(data)

    def decrypt_bytes(self, token: bytes) -> bytes:
        return self.fernet.decrypt(token)

encryption_service = EncryptionService()
