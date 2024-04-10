from airflow import DAG
from conveyor.operators import ConveyorContainerOperatorV2
from datetime import datetime, timedelta


default_args = {
    "owner": "Conveyor",
    "depends_on_past": False,
    "start_date": datetime(year=2024, month=1, day=31),
    "email": [],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "llm-hackathon-ingestion", default_args=default_args, schedule_interval="@monthly", max_active_runs=1
)

ConveyorContainerOperatorV2(
    dag=dag,
    task_id="scrape",
    cmds=["python"],
    arguments=[
        "-m",
        "llmhackathoningestion.sample",
        "--date", "{{ ds }}",
        "--env",
        "{{ macros.conveyor.env() }}",
        "--task",
        "scrape",
        "--bucket",
        "llmhackathon-demo",
    ],
    instance_type="mx.micro",
    aws_role="llm-hackathon-ingestion-{{ macros.conveyor.env() }}",
)
