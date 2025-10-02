import logging

def Logger(name: str) -> logging.Logger:
    """Sets up and returns a logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # Set the logger level to INFO

    # File handler
    file_handler = logging.FileHandler('localsync.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler (optional - for seeing logs in terminal too)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger