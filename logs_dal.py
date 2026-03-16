from datetime import datetime
from .consts import logs_db_path
from .db_utils import execute_with_retry


class LogsDAL:
    def __init__(self, job_id: int, job_type: str):
        self.job_id = job_id
        self.job_type = job_type

    def _write_log(self, log_type: str, message: str):
        """Writes a log entry to the SQLite database."""
        def operation(cursor):
            cursor.execute(
                """
                INSERT INTO logs (timestamp, type, job_id, job_type, message)
                VALUES (?, ?, ?, ?, ?)
                """,
                (datetime.now().isoformat(), log_type, self.job_id, self.job_type, message),
            )

        execute_with_retry(logs_db_path, operation)

    def log_info(self, message: str):
        self._write_log("INFO", message)

    def log_error(self, message: str):
        self._write_log("ERROR", message)

    def log_warning(self, message: str):
        self._write_log("WARNING", message)