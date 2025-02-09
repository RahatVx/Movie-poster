import os

# ======================================================================
# Bot Configuration
# ======================================================================
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")  # Telegram Bot Token
LOGS_CHANNEL = int(os.getenv("LOGS_CHANNEL", "-1001234567890"))  # লগস চ্যানেলের আইডি
SCRAP_CHANNEL = int(os.getenv("SCRAP_CHANNEL", "-1009876543210"))  # পোস্টার সংরক্ষণের চ্যানেল

# ======================================================================
# Admins Configuration
# ======================================================================
# কমা দিয়ে পৃথক করা সকল এডমিন ইউজার আইডি (স্ট্রিং হিসেবে সংরক্ষিত)
ADMIN_USER_IDS = os.getenv("ADMIN_USER_IDS", "123456789,987654321").split(",")

# ======================================================================
# MongoDB Configuration
# ======================================================================
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://username:password@cluster.mongodb.net/myDatabase?retryWrites=true&w=majority")

# ======================================================================
# Channel URLs for UI Buttons
# ======================================================================
MAIN_CHANNEL_URL = os.getenv("MAIN_CHANNEL_URL", "https://t.me/YourMainChannel")
BACKUP_CHANNEL_URL = os.getenv("BACKUP_CHANNEL_URL", "https://t.me/YourBackupChannel")
REQUEST_GROUP_URL = os.getenv("REQUEST_GROUP_URL", "https://t.me/YourRequestGroup")
ADMINS_GROUP_URL = os.getenv("ADMINS_GROUP_URL", "https://t.me/YourAdmins")
SUPPORT_GROUP_URL = os.getenv("SUPPORT_GROUP_URL", "https://t.me/YourSupportGroup")

# ======================================================================
# Feature Flags
# ======================================================================
ENABLE_BATCH_PROCESSING = os.getenv("ENABLE_BATCH_PROCESSING", "True") == "True"
ENABLE_ANALYTICS = os.getenv("ENABLE_ANALYTICS", "True") == "True"
ENABLE_EMAIL_NOTIFICATIONS = os.getenv("ENABLE_EMAIL_NOTIFICATIONS", "False") == "True"

# ======================================================================
# Email Configuration (Dummy for Notification)
# ======================================================================
EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "smtp.example.com")
EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "587"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", "your_email@example.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_email_password")
EMAIL_FROM = os.getenv("EMAIL_FROM", "your_email@example.com")
EMAIL_TO = os.getenv("EMAIL_TO", "notify@example.com")

# ======================================================================
# Logging Configuration
# ======================================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "bot.log")

# ======================================================================
# Other Custom Configurations
# ======================================================================
CUSTOM_GREETING = os.getenv("CUSTOM_GREETING", "স্বাগতম, আপনি Advanced Movie Bot এ আছেন!")
CUSTOM_FOOTER = os.getenv("CUSTOM_FOOTER", "Developed by Your Name. All rights reserved.")

# ======================================================================
# End of config.py
# ======================================================================

# (এই ফাইলটি ভবিষ্যতের জন্য placeholder লাইনসহ প্রসারিত করা হয়েছে)
for _ in range(20):
    pass  # Additional configuration placeholders
