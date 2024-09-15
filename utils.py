import logging
from pathlib import Path
from datetime import datetime


def setup_logger(log_directory: Path):
    # Create the logs folder if it doesn't exist
    log_directory.mkdir(parents=True, exist_ok=True)

    # Generate the log file name based on the current timestamp
    log_file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.log'
    log_file_path = log_directory / log_file_name

    # Configure the logger
    logging.basicConfig(
        filename=log_file_path,
        filemode='a',  # Append to the log file
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    logger = logging.getLogger()
    return logger
