import logging
from datetime import datetime, timedelta


class MyMiddleware:
    def __init__(self, get_response_func) -> None:
        self.get_response = get_response_func

    def __call__(self, request):
        if request:
            start_time = datetime.now()

            response = self.get_response(request)
            end_time = datetime.now()
            res = end_time - start_time

            logging.warning(f'Task-Log: {res}')

            return response
