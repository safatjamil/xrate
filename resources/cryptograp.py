import bcrypt
import cryptography
from cryptography.fernet import Fernet

class Encrypt:

    def hash_password(password):
        return bcrypt.hashpw(password.encode("utf-8"), 
                             bcrypt.gensalt()) 
    
    def string(content):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(content.encode())
        data = {"key": key, "enc_string": encrypted}
        return data


class Decrypt:

    def string(encrypted, key):
        fernet = Fernet(key)
        return fernet.decrypt(encrypted).decode()
