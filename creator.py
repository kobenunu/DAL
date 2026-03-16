import sqlite3


def create_databases(experiments_db_path: str, logs_db_path: str):
    conn = sqlite3.connect(experiments_db_path)
    conn2 = sqlite3.connect(logs_db_path)

    cursor = conn.cursor()
    cursor2 = conn2.cursor()

    create_table_query = '''
CREATE TABLE IF NOT EXISTS tnbc_st_experiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time DATETIME,
    end_time DATETIME,
    status TEXT,
    slurm_job_id TEXT,
    tissue_type TEXT,
    aggregation_type TEXT,
    is_spatial BOOLEAN,
    variance_type TEXT,
    variance_value REAL,
    model_type TEXT,
    seed_count INTEGER,
    mean_auc REAL,
    max_auc REAL,
    permutation_auc REAL,
    config TEXT
)
'''

    cursor.execute(create_table_query)



    create_logs_table_query = '''
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME,
    type TEXT,
    job_id INTEGER,
    job_type TEXT,
    message TEXT
)
'''
    cursor2.execute(create_logs_table_query)


    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_experiments_slurm_job_id
    ON tnbc_st_experiments(slurm_job_id)
''')

    # Index for fast sorting by mean_auc (DESC so the highest AUCs are retrieved fastest)
    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_experiments_mean_auc
    ON tnbc_st_experiments(mean_auc DESC)
''')

    # 3. Create Index for 'logs'
    # Composite index: Equality checks first (job_id, job_type), then range checks (timestamp)
    cursor2.execute('''
    CREATE INDEX IF NOT EXISTS idx_logs_job_lookup
    ON logs(job_id, job_type, timestamp)
''')

    conn.commit()
    cursor.close()
    conn.close()
    conn2.commit()
    cursor2.close()
    conn2.close()
