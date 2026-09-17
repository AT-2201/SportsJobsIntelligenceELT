"""Serve the live Sports Jobs flow on a daily local schedule."""

from prefect.schedules import Cron

from orchestration.prefect_flow import sports_jobs_daily

DAILY_SCHEDULE = Cron("0 6 * * *", timezone="America/Phoenix")


def main() -> None:
    sports_jobs_daily.serve(
        name="sports-jobs-daily-local",
        schedule=DAILY_SCHEDULE,
        description="Daily live sports-jobs ingestion, dbt transformation, and testing.",
        tags=["sports-jobs", "live"],
        pause_on_shutdown=True,
    )


if __name__ == "__main__":
    main()
