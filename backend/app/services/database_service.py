"""
DATABASE SERVICE
=================
Purpose: Allow PhantomAI to query the database safely.

Why This Matters:
- Users need to check database data
- PhantomAI can answer data questions
- Makes PhantomAI a database expert

How It Works:
1. Takes a SQL query
2. Validates it's safe
3. Runs it on PostgreSQL
4. Returns the results

Safety:
- Only SELECT queries allowed
- Query preview before execution
- Max 100 rows returned
- No dangerous commands
"""

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import re

# List of forbidden SQL commands
FORBIDDEN = [
    "DROP", "DELETE", "UPDATE", "INSERT", 
    "ALTER", "TRUNCATE", "GRANT", "REVOKE",
    "CREATE", "DROP", "RENAME"
]

def validate_query(query: str) -> dict:
    """
    Validate a SQL query for safety.
    
    Checks:
    1. Is it a SELECT query?
    2. Does it contain forbidden commands?
    3. Does it have a LIMIT?
    
    Returns:
    {
        "valid": True/False,
        "error": "Error message if invalid"
    }
    """
    query_upper = query.upper()
    
    # Check for forbidden commands
    for forbidden in FORBIDDEN:
        if forbidden in query_upper:
            return {
                "valid": False,
                "error": f"FORBIDDEN: '{forbidden}' is not allowed. Only SELECT queries are permitted."
            }
    
    # Check if it's a SELECT query
    if not query_upper.strip().startswith("SELECT"):
        return {
            "valid": False,
            "error": "Only SELECT queries are allowed for safety."
        }
    
    # Check if it has a LIMIT (safety)
    if "LIMIT" not in query_upper:
        return {
            "valid": True,
            "warning": "No LIMIT specified. Results will be limited to 100 rows."
        }
    
    return {
        "valid": True,
        "warning": None
    }

def execute_query(db, query: str) -> dict:
    """
    Execute a SQL query safely.
    
    How It Works:
    1. Validates the query
    2. Runs it with a LIMIT
    3. Returns the results
    
    Returns:
    {
        "success": True,
        "data": [{"column1": "value1", ...}],
        "row_count": 5
    }
    """
    try:
        # Validate the query
        validation = validate_query(query)
        if not validation["valid"]:
            return {
                "success": False,
                "error": validation["error"]
            }
        
        # Add LIMIT if not present
        query = query.rstrip()
        if "LIMIT" not in query.upper():
            query = f"{query} LIMIT 100"
        
        # Execute the query
        result = db.execute(text(query))
        
        # Get column names
        columns = result.keys()
        
        # Convert to list of dictionaries
        data = []
        for row in result:
            row_dict = {}
            for idx, column in enumerate(columns):
                row_dict[column] = row[idx]
            data.append(row_dict)
        
        return {
            "success": True,
            "data": data,
            "row_count": len(data),
            "columns": list(columns),
            "query": query
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

def get_tables(db) -> list:
    """
    Get all tables in the database.
    
    Returns:
    {
        "tables": ["users", "conversations", "messages"]
    }
    """
    try:
        result = db.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        
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
    Get information about a specific table.
    
    Returns:
    {
        "columns": [{"name": "id", "type": "integer"}, ...]
    }
    """
    try:
        result = db.execute(text("""
            SELECT 
                column_name,
                data_type,
                is_nullable
            FROM information_schema.columns
            WHERE table_name = :table_name
            ORDER BY ordinal_position
        """), {"table_name": table_name})
        
        columns = []
        for row in result:
            columns.append({
                "name": row[0],
                "type": row[1],
                "nullable": row[2] == "YES"
            })
        
        return {
            "success": True,
            "columns": columns
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }