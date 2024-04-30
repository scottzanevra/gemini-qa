import logging
import yaml

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_config(config_file='config.yml'):

    logger.info(f"Loading config {config_file}")

    try:
        with open(config_file) as config_str:
            config = yaml.load(config_str, Loader=yaml.Loader)
    except (IOError, FileNotFoundError):
        logger.exception("Failed to open config file %s", config_file)

    return config


if __name__ == '__main__':
    config = get_config()
