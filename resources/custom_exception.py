class QuizExceptionHandler(Exception):
    def __init__(self, error_msg, error_code):
        self.error_msg = error_msg
        self.error_code = error_code
        super().__init__(self.error_msg)