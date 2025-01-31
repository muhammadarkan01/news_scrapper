import logging

def setup_logger():
    logger = logging.getLogger("Detik Scrapper Log")
    logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # File handler for errors
    error_file_handler = logging.FileHandler("error.log")
    error_file_handler.setLevel(logging.ERROR)

    # File handler for console output
    console_file_handler = logging.FileHandler("console.log")
    console_file_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    error_file_handler.setFormatter(formatter)
    console_file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)  # Logs to the console
    logger.addHandler(error_file_handler)  # Logs errors to error.log
    logger.addHandler(console_file_handler)  # Logs console output to console.log

    return logger
