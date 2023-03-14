from os import getenv

class Config:
    api_hash = getenv("API_HASH", None)
    api_id = int(getenv("API_ID", 12345))
    bot_token = getenv("BOT_TOKEN", "")
    database_url = getenv("DATABASE_URL", "")
    force_sub = getenv("FORCE_SUB", None)
    log_channel = getenv("LOG_CHANNEL", None)
    owner = list(int(user) for user in getenv("OWNER_ID", "").split(' '))
    
