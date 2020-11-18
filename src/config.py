# coding=utf-8
import sec

LOG_LEVEL = sec.load("log_level", fallback="INFO").upper()

# Flask
DEBUG = False

# Flask Redis
REDIS_URL = sec.load("redis_url", fallback="redis://localhost")

# Flack
FLACK_DEFAULT_NAME = "Unit Converter"
FLACK_URL_PREFIX = sec.load("flack_prefix", fallback="/")

FLACK_TOKEN = sec.load("slack_token")
FLACK_CLIENT_ID = sec.load("slack_client_id")
FLACK_CLIENT_SECRET = sec.load("slack_app_secret")
