"""
PhantomAI Database Service

Read-only database explorer.

Security rules:
- SELECT statements only
- One SQL statement per request
- Maximum 100 returned rows
- No INSERT/UPDATE/DELETE/DROP/etc.
- Password/credential columns are never exposed
- Database metadata is restricted to public schema
"""

import re

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


MAX_ROWS = 100

FORBIDDEN_COMMANDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE",
    "RENAME",
    "COMMENT",
    "VACUUM",
    "ANALYZE",
    "CALL",
    "DO",
}

# Never expose credential material through the explorer.
SENSITIVE_COLUMNS = {
    "password",
    "password_hash",
    "hashed_password",
    "passwd",
    "passhash",
    "secret",
    "secret_key",
    "api_key",
    "access_token",
    "refresh_token",
    "token",
    "private_key",
}


def validate_query(query: str) -> dict:
    """
    Validate an incoming SQL query.

    Only one SELECT statement is permitted.
    """

    if not isinstance(query, str):
        return {
            "valid": False,
            "error": "Query must be a string."
        }

    query = query.strip()

    if not query:
        return {
            "valid": False,
            "error": "Query cannot be empty."
        }

    # Remove one trailing semicolon for validation.
    cleaned = query.rstrip(";").strip()

    # Reject multiple statements.
    if ";" in cleaned:
        return {
            "valid": False,
            "error": "Multiple SQL statements are not allowed."
        }

    query_upper = cleaned.upper()

    # Must begin with SELECT.
    if not re.match(r"^SELECT\b", query_upper):
        return {
            "valid": False,
            "error": "Only SELECT queries are permitted."
        }

    # Block dangerous SQL keywords.
    for command in FORBIDDEN_COMMANDS:
        if re.search(rf"\b{re.escape(command)}\b", query_upper):
            return {
                "valid": False,
                "error": (
                    f"FORBIDDEN: '{command}' is not allowed. "
                    "Only SELECT queries are permitted."
                )
            }

    return {
        "valid": True,
        "query": cleaned
    }


def _contains_sensitive_column(query: str) -> str | None:
    """
    Detect explicit references to protected credential columns.

    This intentionally blocks explicit credential access rather than
    trying to infer whether the caller 'should' be allowed to see hashes.
    """

    for column in SENSITIVE_COLUMNS:
        if re.search(
            rf"\b{re.escape(column)}\b",
            query,
            re.IGNORECASE
        ):
            return column

    return None


def _enforce_limit(query: str) -> str:
    """
    Ensure query returns at most MAX_ROWS rows.
    """

    # Existing numeric LIMIT
    limit_match = re.search(
        r"\bLIMIT\s+(\d+)",
        query,
        re.IGNORECASE
    )

    if limit_match:
        requested_limit = int(limit_match.group(1))

        if requested_limit > MAX_ROWS:
            query = re.sub(
                r"\bLIMIT\s+\d+",
                f"LIMIT {MAX_ROWS}",
                query,
                count=1,
                flags=re.IGNORECASE
            )

        return query

    # No LIMIT supplied.
    return f"{query} LIMIT {MAX_ROWS}"


def execute_query(db, query: str) -> dict:
    """
    Execute a safe read-only SELECT query.
    """

    try:

        # --------------------------------------------------
        # VALIDATE
        # --------------------------------------------------

        validation = validate_query(query)

        if not validation["valid"]:
            return {
                "success": False,
                "error": validation["error"]
            }

        query = validation["query"]

        # --------------------------------------------------
        # PROTECT SENSITIVE COLUMNS
        # --------------------------------------------------

        sensitive_column = _contains_sensitive_column(query)

        if sensitive_column:
            return {
                "success": False,
                "error": (
                    f"Access to sensitive column "
                    f"'{sensitive_column}' is not permitted "
                    "through the database explorer."
                )
            }

        # --------------------------------------------------
        # LIMIT RESULTS
        # --------------------------------------------------

        query = _enforce_limit(query)

        # --------------------------------------------------
        # EXECUTE
        # --------------------------------------------------

        result = db.execute(text(query))

        columns = list(result.keys())

        data = []

        for row in result:
            row_dict = {}

            for index, column in enumerate(columns):
                row_dict[column] = row[index]

            data.append(row_dict)

        return {
            "success": True,
            "data": data,
            "row_count": len(data),
            "columns": columns,
            "query": query,
            "max_rows": MAX_ROWS
        }

    except SQLAlchemyError as e:

        return {
            "success": False,
            "error": str(e)
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


def get_tables(db) -> dict:
    """
    Return tables from the public schema.
    """

    try:

        result = db.execute(
            text(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
                """
            )
        )

        tables = [row[0] for row in result]

        return {
            "success": True,
            "tables": tables
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


def get_table_info(db, table_name: str) -> dict:
    """
    Return safe structural information about a table.
    """

    try:

        result = db.execute(
            text(
                """
                SELECT
                    column_name,
                    data_type,
                    is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'public'
                AND table_name = :table_name
                ORDER BY ordinal_position
                """
            ),
            {
                "table_name": table_name
            }
        )

        columns = []

        for row in result:

            column_name = row[0]

            columns.append(
                {
                    "name": column_name,
                    "type": row[1],
                    "nullable": row[2] == "YES",
                    "sensitive": (
                        column_name.lower()
                        in SENSITIVE_COLUMNS
                    )
                }
            )

        if not columns:
            return {
                "success": False,
                "error": f"Table '{table_name}' was not found."
            }

        return {
            "success": True,
            "table": table_name,
            "columns": columns
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }