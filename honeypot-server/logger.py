import logging
import os
import re

# ============================
#     SANITIZE SENSITIVE DATA
# ============================
class CredentialFilter(logging.Filter):
    def filter(self, record):
        record.msg = re.sub(
            r"(password|token|api_key|key)=\S+",
            r"\1=****",
            str(record.msg),
            flags=re.IGNORECASE
        )
        return True


# ============================
#     LOGS DIRECTORY
# ============================
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# ============================
#     AUTH LOGGER
# ============================
auth_logger = logging.getLogger("auth_logger")
auth_logger.setLevel(logging.INFO)

auth_handler = logging.FileHandler(os.path.join(LOG_DIR, "auth.log"))
auth_handler.setFormatter(logging.Formatter("%(asctime)s | AUTH | %(message)s"))
auth_handler.addFilter(CredentialFilter())
auth_logger.addHandler(auth_handler)


# ============================
#     COMMAND LOGGER
# ============================
cmd_logger = logging.getLogger("cmd_logger")
cmd_logger.setLevel(logging.INFO)

cmd_handler = logging.FileHandler(os.path.join(LOG_DIR, "commands.log"))
cmd_handler.setFormatter(logging.Formatter("%(asctime)s | CMD | %(message)s"))
cmd_handler.addFilter(CredentialFilter())
cmd_logger.addHandler(cmd_handler)


# ============================
#     PUBLIC FUNCTIONS
# ============================
def log_auth(username, password):
    auth_logger.info(f"user={username} password={password}")


def log_cmd(command, output):
    # remove linebreaks to keep logs clean
    output = output.replace("\n", "\\n")
    cmd_logger.info(f"command={command} output={output}")
