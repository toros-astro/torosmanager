import yaml as _yaml

CONFIG_PATH = "/etc/toros/toros.conf.yaml"
_CONFIG_IS_LOADED = False
_config = {}


def load_config():
    global _config
    with open(CONFIG_PATH) as f:
        _config = _yaml.full_load(f.read())


def get_config():
    global _CONFIG_IS_LOADED
    global _config
    if not _CONFIG_IS_LOADED:
        load_config()
        _CONFIG_IS_LOADED = True
    return _config


def get_config_for_key(key):
    config = get_config()
    return config.get(key)


def init_logger():
    import logging

    log_config = get_config_for_key("Logging") or {}
    log_file = log_config.get("File")
    if log_file is None:
        raise ValueError("Logging file undefined.")
    log_level = log_config.get("Log Level") or "INFO"

    # Add a file logger that rotates every 1 day
    # and keeps files for at most 20 days
    # format="{time} {level} {name}: {message}",

    # Then log this:
    logger.info("TOROS manager started.")
    logger.info("Logger level set to {}".format(log_level))

    # Add logger that sends email on ERRORs
    email_conf = get_config_for_key("Email Configuration")
    if email_conf.get("Login Required"):
        credentials = (email_conf.get("Username"), email_conf.get("Password"))
    else:
        credentials = None
    from logging.handlers import SMTPHandler

    emailHandler = SMTPHandler(
        mailhost=(email_conf.get("SMTP Domain"), email_conf.get("SMTP Port")),
        fromaddr=email_conf.get("Sender Address"),
        toaddrs=get_config_for_key("Admin Emails"),
        subject="[ERROR] lvcgcnd failure",
        credentials=credentials,
    )
    logger.add(emailHandler, level="ERROR")


def init_database():
    # Connect to database
    ...
