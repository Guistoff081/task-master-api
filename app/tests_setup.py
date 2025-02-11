import logging

from sqlalchemy import Engine
from sqlmodel import Session, select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init(db_engine: Engine) -> None:
    """
    Initializes the test database connection in the same way as the production code.
    Executes a simple query and commits the transaction to ensure there are no open
    transactions left.
    """
    try:
        # Try to create session to check if DB is awake
        with Session(db_engine) as session:
            # Execute the test health-check query.
            session.exec(select(1))
            # Commit to end the transaction and silence warnings.
            session.commit()
            logger.info("Test database connection established successfully.")
    except Exception as exc:
        logger.error(f"Test database connection failed: {exc}", exc_info=exc)
        raise


def main() -> None:
    logger.info("Initializing service")
    init(engine)
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
