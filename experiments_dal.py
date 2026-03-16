from datetime import datetime
from .db_utils import execute_with_retry


class ExperimentsDAL:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def insert_experiment(
        self,
        slurm_job_id: str,
        tissue_type: str,
        aggregation_type: str,
        is_spatial: bool,
        variance_type: str,
        variance_value: float,
        model_type: str,
        seed_count: int,
        config: str,
    ):
        def operation(cursor):
            cursor.execute(
                """
                INSERT INTO tnbc_st_experiments
                    (start_time, end_time, status, slurm_job_id,
                     tissue_type, aggregation_type, is_spatial,
                     variance_type, variance_value, model_type,
                     seed_count, mean_auc, max_auc, permutation_auc, config)
                VALUES (?, NULL, 'running', ?, ?, ?, ?, ?, ?, ?, ?, -1, -1, -1, ?)
                """,
                (
                    datetime.now().isoformat(),
                    slurm_job_id,
                    tissue_type,
                    aggregation_type,
                    is_spatial,
                    variance_type,
                    variance_value,
                    model_type,
                    seed_count,
                    config,
                ),
            )

        execute_with_retry(self.db_path, operation)

    def update_experiment(
        self,
        id: int,
        mean_auc: float,
        max_auc: float,
        permutation_auc: float,
    ):
        def operation(cursor):
            cursor.execute(
                """
                UPDATE tnbc_st_experiments
                SET end_time = ?, status = 'ended',
                    mean_auc = ?, max_auc = ?, permutation_auc = ?
                WHERE id = ?
                """,
                (datetime.now().isoformat(), mean_auc, max_auc, permutation_auc, id),
            )

        execute_with_retry(self.db_path, operation)
