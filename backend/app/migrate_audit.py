from sqlalchemy import text

from backend.app.database.database import engine


def main():
    print("Updating audit_logs table...")

    statements = [
        """
        ALTER TABLE audit_logs
        ADD COLUMN IF NOT EXISTS organization VARCHAR(255)
        """,
        """
        ALTER TABLE audit_logs
        ADD COLUMN IF NOT EXISTS role VARCHAR(100)
        """,
        """
        ALTER TABLE audit_logs
        ADD COLUMN IF NOT EXISTS query TEXT
        """,
        """
        ALTER TABLE audit_logs
        ADD COLUMN IF NOT EXISTS success BOOLEAN DEFAULT TRUE
        """,
    ]

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))

    print("audit_logs table updated successfully!")


if __name__ == "__main__":
    main()
