"""
Staff Database Access Router
============================

Purpose:
    Provide authorized PhantomAI staff with controlled,
    read-only access to connected PostgreSQL databases.

Security:
    - User must be authenticated.
    - User must have is_staff=True.
    - User must have an authorized role.
    - Only SELECT statements are accepted.
    - Multiple SQL statements are rejected.
    - INSERT/UPDATE/DELETE/DROP/etc. are rejected.
    - Maximum 100 returned rows.
    - Password/credential columns are never returned.
    - Table metadata is restricted to the public schema.
"""

import re

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User


router = APIRouter(
    prefix="/staff/database",
    tags=["Staff Database"],
)


# ============================================================
# CONFIGURATION
# ============================================================

MAX_ROWS = 100

AUTHORIZED_ROLES = {
    "admin",
    "staff",
    "analyst",
    "investigator",
}

# Columns that should NEVER be exposed through this API.
#
# This is deliberately broader than just "password".
# Different organizations may use different names.
SENSITIVE_COLUMNS = {
    "password",
    "password_hash",
    "passwd",
    "pass_hash",
    "secret",
    "secret_key",
    "api_key",
    "access_token",
    "refresh_token",
    "private_key",
    "encryption_key",
    "credential",
    "credentials",
}


FORBIDDEN_COMMANDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "GRANT",
    "REVOKE",
    "CREATE",
    "RENAME",
    "MERGE",
    "UPSERT",
    "CALL",
    "EXEC",
    "EXECUTE",
}


# ============================================================
# REQUEST MODEL
# ============================================================

class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Read-only SQL SELECT query.",
    )


# ============================================================
# STAFF AUTHORIZATION
# ============================================================

def require_staff(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Require an authenticated staff member.

    Access requires:
        is_staff = True

    And an authorized role.
    """

    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Authentication required.",
        )

    if not getattr(current_user, "is_staff", False):
        raise HTTPException(
            status_code=403,
            detail="Staff authorization required.",
        )

    role = (getattr(current_user, "role", "") or "").lower()

    if role not in AUTHORIZED_ROLES:
        raise HTTPException(
            status_code=403,
            detail="Your staff role is not authorized for database access.",
        )

    return current_user


# ============================================================
# QUERY NORMALIZATION
# ============================================================

def normalize_query(query: str) -> str:
    """
    Normalize whitespace and remove trailing semicolon.
    """

    query = query.strip()

    # Remove trailing semicolons only.
    query = query.rstrip(";").strip()

    return query


# ============================================================
# QUERY VALIDATION
# ============================================================

def validate_query(query: str) -> dict:
    """
    Validate a database query.

    Requirements:
        - Must not be empty.
        - Must be one SQL statement.
        - Must begin with SELECT.
        - No dangerous SQL commands.
        - No comments.
        - No sensitive credential columns.
    """

    if not query or not query.strip():
        return {
            "valid": False,
            "error": "Query cannot be empty.",
        }

    query = normalize_query(query)

    # --------------------------------------------------------
    # Reject multiple statements
    # --------------------------------------------------------

    if ";" in query:
        return {
            "valid": False,
            "error": "Multiple SQL statements are not allowed.",
        }

    # --------------------------------------------------------
    # Reject SQL comments
    #
    # This makes query inspection substantially safer.
    # --------------------------------------------------------

    if "--" in query or "/*" in query or "*/" in query:
        return {
            "valid": False,
            "error": "SQL comments are not allowed.",
        }

    query_upper = query.upper().strip()

    # --------------------------------------------------------
    # SELECT only
    # --------------------------------------------------------

    if not query_upper.startswith("SELECT"):
        return {
            "valid": False,
            "error": "Only SELECT queries are permitted.",
        }

    # --------------------------------------------------------
    # Make sure SELECT is actually a standalone keyword.
    #
    # Prevent things like:
    # SELECTED ...
    # --------------------------------------------------------

    if not re.match(r"^SELECT\b", query_upper):
        return {
            "valid": False,
            "error": "Only SELECT queries are permitted.",
        }

    # --------------------------------------------------------
    # Forbidden SQL commands
    # --------------------------------------------------------

    for command in FORBIDDEN_COMMANDS:

        pattern = rf"\b{re.escape(command)}\b"

        if re.search(pattern, query_upper):
            return {
                "valid": False,
                "error": (
                    f"FORBIDDEN: '{command}' is not allowed. "
                    "Only SELECT queries are permitted."
                ),
            }

    # --------------------------------------------------------
    # Prevent PostgreSQL locking queries.
    # --------------------------------------------------------

    if re.search(r"\bFOR\s+(UPDATE|NO\s+KEY\s+UPDATE|SHARE|KEY\s+SHARE)\b",
                 query_upper):

        return {
            "valid": False,
            "error": "Row-locking queries are not permitted.",
        }

    # --------------------------------------------------------
    # Prevent obvious database functions that can cause
    # side effects or deliberate delays.
    # --------------------------------------------------------

    dangerous_functions = [
        "PG_SLEEP",
        "PG_ADVISORY_LOCK",
        "PG_ADVISORY_XACT_LOCK",
        "PG_TERMINATE_BACKEND",
        "PG_CANCEL_BACKEND",
    ]

    for function_name in dangerous_functions:

        if re.search(
            rf"\b{re.escape(function_name)}\s*\(",
            query_upper,
        ):
            return {
                "valid": False,
                "error": (
                    f"Database function '{function_name}' "
                    "is not permitted."
                ),
            }

    # --------------------------------------------------------
    # Sensitive credential fields
    # --------------------------------------------------------

    for column in SENSITIVE_COLUMNS:

        if re.search(
            rf"\b{re.escape(column)}\b",
            query,
            re.IGNORECASE,
        ):
            return {
                "valid": False,
                "error": (
                    f"Access to sensitive column '{column}' "
                    "is not permitted for this database role."
                ),
            }

    return {
        "valid": True,
        "warning": None,
    }


# ============================================================
# APPLY ROW LIMIT
# ============================================================

def enforce_limit(query: str) -> str:
    """
    Enforce a maximum of MAX_ROWS rows.

    Examples:

        SELECT * FROM users

    becomes:

        SELECT * FROM users LIMIT 100

    And:

        SELECT * FROM users LIMIT 500

    becomes:

        SELECT * FROM users LIMIT 100
    """

    query = normalize_query(query)

    limit_match = re.search(
        r"\bLIMIT\s+(\d+)\b",
        query,
        re.IGNORECASE,
    )

    if limit_match:

        requested_limit = int(limit_match.group(1))

        if requested_limit > MAX_ROWS:

            query = re.sub(
                r"\bLIMIT\s+\d+\b",
                f"LIMIT {MAX_ROWS}",
                query,
                count=1,
                flags=re.IGNORECASE,
            )

    else:

        query = f"{query} LIMIT {MAX_ROWS}"

    return query


# ============================================================
# SANITIZE RESULT
# ============================================================

def sanitize_result(columns, row):
    """
    Convert a SQLAlchemy row into a safe dictionary.

    Sensitive fields are never returned.
    """

    output = {}

    for index, column in enumerate(columns):

        column_name = str(column)

        if column_name.lower() in SENSITIVE_COLUMNS:
            continue

        output[column_name] = row[index]

    return output


# ============================================================
# EXECUTE QUERY
# ============================================================

def execute_staff_query(
    db: Session,
    query: str,
) -> dict:
    """
    Execute an authorized read-only SELECT query.
    """

    try:

        # ----------------------------------------------------
        # Validate
        # ----------------------------------------------------

        validation = validate_query(query)

        if not validation["valid"]:

            return {
                "success": False,
                "error": validation["error"],
            }

        # ----------------------------------------------------
        # Enforce maximum rows
        # ----------------------------------------------------

        query = enforce_limit(query)

        # ----------------------------------------------------
        # Execute
        # ----------------------------------------------------

        result = db.execute(text(query))

        columns = list(result.keys())

        # ----------------------------------------------------
        # Build safe response
        # ----------------------------------------------------

        data = []

        for row in result:

            data.append(
                sanitize_result(columns, row)
            )

        safe_columns = [
            column
            for column in columns
            if column.lower() not in SENSITIVE_COLUMNS
        ]

        return {
            "success": True,
            "data": data,
            "row_count": len(data),
            "columns": safe_columns,
            "query": query,
            "max_rows": MAX_ROWS,
        }

    except SQLAlchemyError as exc:

        return {
            "success": False,
            "error": str(exc),
        }

    except Exception as exc:

        return {
            "success": False,
            "error": str(exc),
        }


# ============================================================
# GET TABLES
# ============================================================

@router.get("/tables")
def list_tables(
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db),
):
    """
    Return tables available in the public schema.
    """

    try:

        result = db.execute(
            text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """)
        )

        tables = [row[0] for row in result]

        return {
            "success": True,
            "tables": tables,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve tables: {str(exc)}",
        )


# ============================================================
# GET TABLE INFORMATION
# ============================================================

@router.get("/table/{table_name}")
def table_info(
    table_name: str,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db),
):
    """
    Return column information for a public table.
    """

    try:

        result = db.execute(
            text("""
                SELECT
                    column_name,
                    data_type,
                    is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = :table_name
                ORDER BY ordinal_position
            """),
            {
                "table_name": table_name,
            },
        )

        columns = []

        for row in result:

            column_name = row[0]

            # Do not expose credential columns.
            if column_name.lower() in SENSITIVE_COLUMNS:
                continue

            columns.append({
                "name": column_name,
                "type": row[1],
                "nullable": row[2] == "YES",
            })

        if not columns:

            raise HTTPException(
                status_code=404,
                detail=f"Table '{table_name}' was not found "
                       "or contains no accessible columns.",
            )

        return {
            "success": True,
            "table": table_name,
            "columns": columns,
        }

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to inspect table: {str(exc)}",
        )


# ============================================================
# RUN STAFF QUERY
# ============================================================

@router.post("/query")
def run_staff_query(
    request: QueryRequest,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db),
):
    """
    Execute a read-only database query.

    Only authorized staff can use this endpoint.
    """

    result = execute_staff_query(
        db=db,
        query=request.query,
    )

    if not result["success"]:

        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )

    return result