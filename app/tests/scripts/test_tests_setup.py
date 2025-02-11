from unittest.mock import MagicMock, patch

from sqlmodel import select

from app.tests_setup import init, logger


def test_init_successful_connection() -> None:
    engine_mock = MagicMock()

    session_mock = MagicMock()
    # Make the context manager return our session_mock
    session_mock.__enter__.return_value = session_mock
    session_mock.exec = MagicMock(return_value=True)
    session_mock.commit = MagicMock()

    # Patch the Session in the module where it is used (not in sqlmodel)
    with (
        patch("app.tests_setup.Session", return_value=session_mock),
        patch.object(logger, "info"),
        patch.object(logger, "error"),
        patch.object(logger, "warn"),
    ):
        try:
            init(engine_mock)
        except Exception:
            raise AssertionError(
                "The database connection should be successful and not raise an exception."
            )

        # Assert that the exec function was called exactly once with select(1)
        session_mock.exec.assert_called_once()
        # Get the argument passed to exec
        args, _ = session_mock.exec.call_args
        # Compare string representations to avoid instance inequality issues
        assert str(args[0]) == str(select(1)), (
            "The session should execute a select statement once."
        )
