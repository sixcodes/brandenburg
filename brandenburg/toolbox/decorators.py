# coding=utf-8
import logging
from json import dumps


def log_exception_command(method_to_decorate):

    logger = logging.getLogger("command")

    def wrapper(self, *args, **kwargs):
        logger.info(f"Starting {self.__class__.__module__}")
        try:
            return method_to_decorate(self, *args, **kwargs)
        except Exception as e:
            logger.exception(f"{self.__class__.__module__} with {e}")
            raise

    return wrapper


def log_exception_command_with_logger_name(logger_name="command"):
    def _wrap(method_to_decorate):
        logger = logging.getLogger(logger_name)

        def wrapper(self, *args, **kwargs):
            logger.info(f"Iniciando {self.__class__.__module__} ")
            try:
                return method_to_decorate(self, *args, **kwargs)
            except Exception as e:
                logger.exception(f"{self.__class__.__module__} with {e}")
                raise

        return wrapper

    return _wrap


def check_permission_ajax(method_to_decorate):
    def continue_or_not_authorized(obj, request, *args, **kwargs):
        obj.is_authenticated(request)
        obj.is_authorized(request)
        obj.throttle_check(request)
        return method_to_decorate(obj, request, *args, **kwargs)

    return continue_or_not_authorized
