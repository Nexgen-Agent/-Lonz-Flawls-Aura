# backend/crypto/key_manager.py

import hashlib
from backend.config import settings

class KeyManager:
    """
    Manages cryptographic keys for various parts of the application.

    This class ensures that different domains use derived, specific keys
    instead of sharing the master key directly.
    """

    def __init__(self, master_key: str):
        """
        Initializes the KeyManager with a master encryption key.

        Args:
            master_key (str): The master key from the application settings.
        """
        self.master_key = master_key.encode('utf-8')

    def get_derived_key(self, domain: str, salt: str = "default_salt") -> bytes:
        """
        Derives a specific key for a given domain.

        This uses a key derivation function (KDF) to create a unique key
        for a specific purpose, which is more secure than using the master
        key everywhere.

        Args:
            domain (str): The domain for which to derive a key (e.g., 'innovation_ledger').
            salt (str): A salt to add entropy. Should be unique per domain.

        Returns:
            bytes: A derived key for the specified domain.
        """
        domain_specific_salt = (salt + domain).encode('utf-8')
        derived_key = hashlib.pbkdf2_hmac(
            'sha256',
            self.master_key,
            domain_specific_salt,
            100000, # Number of iterations
            dklen=32 # Desired key length in bytes
        )
        return derived_key

# --- New Innovation-Specific Crypto Function ---

def get_innovation_ledger_key() -> bytes:
    """
    A dedicated function to retrieve the cryptographic key for the innovation ledger.

    This demonstrates the integration of the new module with the crypto layer,
    ensuring that sensitive data in the innovation domain is encrypted with its
    own derived key.
    """
    key_manager = KeyManager(master_key=settings.MASTER_ENCRYPTION_KEY)
    print("Derived a new cryptographic key for the Innovation Ledger.")
    return key_manager.get_derived_key(
        domain="innovation_ledger",
        salt="a-unique-salt-for-innovation"
    )

# You would use this key to encrypt/sign ledger entries:
# ledger_key = get_innovation_ledger_key()
# encrypted_data = encrypt(data, ledger_key)
