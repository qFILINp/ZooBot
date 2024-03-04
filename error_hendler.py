import logging


async def handle_errors(func, *args, **kwargs):
    try:
        await func(*args, **kwargs)
    except Exception as e:
        logging.error(f'Error occurred in function {func.__name__}: {e}', exc_info=True)
