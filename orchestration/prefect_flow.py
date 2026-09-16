"""Deploy this flow with Prefect when scheduled orchestration is desired."""

from prefect import flow, task

from sports_jobs.pipeline import ingest, transform


@task(retries=2, retry_delay_seconds=30)
def ingest_task() -> dict[str, object]:
    return ingest()


@task
def transform_task() -> None:
    transform()


@flow(name="sports-jobs-daily", log_prints=True)
def sports_jobs_daily() -> dict[str, object]:
    ingestion_future = ingest_task.submit()
    transformation_future = transform_task.submit(wait_for=[ingestion_future])

    # Wait for the entire ELT workflow before returning the ingestion summary.
    transformation_future.result()
    return ingestion_future.result()


if __name__ == "__main__":
    sports_jobs_daily()
