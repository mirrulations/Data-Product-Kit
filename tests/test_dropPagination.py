import pytest
from unittest.mock import MagicMock
import os
import sys

# Ensure project root is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sql.DeletePagination import _drop_table_last_week


@pytest.fixture
def mock_conn():
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    return mock_conn, mock_cursor


def test_table_does_not_exist(mock_conn):
    conn, cursor = mock_conn
    cursor.fetchone.return_value = (False,)

    _drop_table_last_week(conn, "nonexistent_table")

    cursor.execute.assert_called_once_with(
        "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'nonexistent_table');"
    )
    conn.commit.assert_not_called()


def test_table_exists_and_deletes_old_records(mock_conn):
    conn, cursor = mock_conn
    cursor.fetchone.return_value = (True,)

    _drop_table_last_week(conn, "test_table")

    assert cursor.execute.call_count == 2
    assert "DELETE FROM test_table WHERE created_at <" in cursor.execute.call_args_list[1][0][0]
    conn.commit.assert_called_once()


def test_error_handling(mock_conn, capsys):
    conn, cursor = mock_conn
    cursor.fetchone.side_effect = Exception("DB error")

    _drop_table_last_week(conn, "test_table")

    captured = capsys.readouterr()
    assert "An error occurred while deleting records from table 'test_table'" in captured.out
