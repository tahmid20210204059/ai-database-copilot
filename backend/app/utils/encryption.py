from cryptography.fernet import Fernet

from ..config import settings


class EncryptionService:
    """
    Handles encryption and decryption of sensitive data.
    """

    def __init__(self):
        self.cipher = Fernet(
            settings.FERNET_KEY.encode()
        )


    def encrypt(self, value: str) -> str:
        """
        Encrypt plain text.
        """

        encrypted = self.cipher.encrypt(
            value.encode()
        )

        return encrypted.decode()


    def decrypt(self, encrypted_value: str) -> str:
        """
        Decrypt encrypted text.
        """

        decrypted = self.cipher.decrypt(
            encrypted_value.encode()
        )

        return decrypted.decode()


encryption_service = EncryptionService()