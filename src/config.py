# coding=utf-8
import sec

LOG_LEVEL = sec.load("log_level", fallback="INFO").upper()

# Flask
DEBUG = False

# Flask Redis
REDIS_URL = sec.load("redis_url", fallback="redis://localhost")

# Flack
FLACK_DEFAULT_NAME = "UnitConverter"
FLACK_TOKEN = sec.load("slack_token")
FLACK_URL_PREFIX = sec.load("flack_prefix", fallback="/")
