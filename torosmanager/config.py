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
    from logging import StreamHandler
    from logging.handlers import TimedRotatingFileHandler, SMTPHandler

    logger = logging.getLogger()
    # Change to DEBUG because default level is WARNING
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
    )

    # Create stdout handler
    stderr_handler = StreamHandler()
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(formatter)
    logger.addHandler(stderr_handler)

    # Create a timed rotating file handler
    # Create a new file every day at midnight and keep only the last 30 files
    log_config = get_config_for_key("Logging") or {}
    log_file = log_config.get("File")
    if log_file is not None:
        log_level_str = log_config.get("Log Level") or "INFO"
        log_level = getattr(logging, log_level_str.upper())
        file_handler = TimedRotatingFileHandler(
            log_file, when="midnight", interval=1, backupCount=30
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Send emails for exceptions and errors
    email_conf = get_config_for_key("Email Configuration")
    if email_conf:
        if email_conf.get("Login Required"):
            credentials = (email_conf.get("Username"), email_conf.get("Password"))
        else:
            credentials = None

        email_handler = SMTPHandler(
            mailhost=(email_conf.get("SMTP Domain"), email_conf.get("SMTP Port")),
            fromaddr=email_conf.get("Sender Address"),
            toaddrs=get_config_for_key("Admin Emails"),
            subject="[ERROR] lvcgcnd failure",
            credentials=credentials,
        )
        email_handler.setLevel(logging.ERROR)
        logger.add(email_handler)


def init_database():
    # Connect to database
    ...
