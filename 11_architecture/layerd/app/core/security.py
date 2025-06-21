import hashlib
from datetime import datetime


class PasswordManager:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return PasswordManager.hash_password(plain_password) == hashed_password


class SecurityUtils:
    @staticmethod
    def generate_session_token() -> str:
        """Generate simple session token"""
        current_time = datetime.now().isoformat()
        return hashlib.md5(current_time.encode()).hexdigest()

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Basic email validation"""
        return "@" in email and "." in email.split("@")[-1]
