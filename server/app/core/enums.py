from enum import Enum


class UserRole(str, Enum):
    USER = "user"                # Regular user (default)
    MODERATOR = "moderator"      # Manages content (e.g., delete posts)
    ADMIN = "admin"              # Manages users, settings, etc.
    SUPER_ADMIN = "super_admin"  # Full system access (rarely used)

class UserStatus(str, Enum):
    PENDING = "pending"          # Awaiting email/phone verification
    ACTIVE = "active"            # Verified and fully accessible
    BLOCKED = "blocked"          # Temporary suspension (e.g., too many failed logins)
    DISABLED = "disabled"        # Manual deactivation by admin (reversible)
    DELETED = "deleted"          # Soft-deleted (GDPR compliance; irreversible)


class OTPStatus(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    EXPIRED = "expired"

class OTPUsage(str, Enum):
    LOGIN = "login"
    PASSWORD_RESET = "password_reset"
    EMAIL_VERIFICATION = "email_verification"
