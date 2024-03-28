from logger import get_logger


class LogException:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        try:
            return self.func()
        except Exception as e:
            logger = get_logger(__name__)
            logger.error(e)
