import logging

def get_logger():
    """Set up and return a logger instance."""
    logging.basicConfig(
        level=logging.INFO,  # Show INFO and above
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    logger = logging.getLogger(__name__)
    return logger
