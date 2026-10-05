"""All tunable settings in one place."""

DAILY_TARGET_PCT = 14.0        # target usage per day (7 days -> 98%)
WEEK_DAYS = 7
MOOD_BAND_PCT = 5.0            # +/- this many points counts as "on pace"
POLL_SECONDS = 300             # how often to ask the server (5 min)
USAGE_URL = "https://api.anthropic.com/api/oauth/usage"
OAUTH_BETA = "oauth-2025-04-20"
CLAUDE_DIR_DEFAULT = "~/.claude"      # overridden by the CLAUDE_CONFIG_DIR env var
CREDENTIALS_FILE = ".credentials.json"

# Personality
CHATTER_MINUTES = (45, 75)     # random chatter every 45-75 minutes
QUIET_HOURS = (22, 8)          # no sounds from 22:00 to 08:00 (except when poked)
BUBBLE_SECONDS = 5             # how long a speech bubble stays
