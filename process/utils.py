
from os.path import join
from logging import INFO, Formatter, StreamHandler, basicConfig, getLogger
from datetime import datetime


def setup_logging(workdir: str = "/tmp", start_utc: datetime = datetime.utcnow()):
    """set up logging system for tasks

    Returns:
        object: a logging object
    """
    formatter = Formatter("%(asctime)s - %(name)s.%(lineno)d - %(levelname)s - %(message)s")
    ch = StreamHandler()
    ch.setLevel(INFO)
    ch.setFormatter(formatter)
    logger_path = join(workdir, f"june_nz.{start_utc.strftime('%Y%m%d')}")
    basicConfig(filename=logger_path),
    logger = getLogger()
    logger.setLevel(INFO)
    logger.addHandler(ch)

    return logger

