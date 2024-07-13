import logging
import os
import sys
from functools import wraps


class ModuleFilter(logging.Filter):
    def __init__(self, module_name):
        super().__init__()
        self.module_name = module_name

    def filter(self, record):
        return record.name.startswith(self.module_name)

def get_logger(name):
    logger = logging.getLogger(name)
    return logger

def setup_logging(debug_mode=False):
    # ログディレクトリの作成
    os.makedirs("log", exist_ok=True)

    # ルートロガーの設定
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)

    # フォーマッターの作成
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # stdoutへのハンドラ
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    stdout_handler.setFormatter(formatter)
    root_logger.addHandler(stdout_handler)

    # debug.logへのハンドラ
    debug_handler = logging.FileHandler("log/debug.log")
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)
    root_logger.addHandler(debug_handler)

    # error.logへのハンドラ
    error_handler = logging.FileHandler("log/error.log")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)

    # llm_summarizer.logへのハンドラ
    llm_summarizer_handler = logging.FileHandler("log/llm_summarizer.log")
    llm_summarizer_handler.setLevel(logging.DEBUG)
    llm_summarizer_handler.setFormatter(formatter)
    
    # フィルターの追加
    llm_summarizer_filter = ModuleFilter(module_name='llm_summarizer')
    llm_summarizer_handler.addFilter(llm_summarizer_filter)
    
    root_logger.addHandler(llm_summarizer_handler)


def log_function_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.debug(f"Calling function: {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


def retry_on_exception(max_retries=3, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger = logging.getLogger(func.__module__)
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt == max_retries - 1:
                        logger.error(f"All {max_retries} attempts failed")
                        raise

        return wrapper

    return decorator