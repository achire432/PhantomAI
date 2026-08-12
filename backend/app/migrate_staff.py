from sqlalchemy import text

from backend.app.database.database import engine


def migrate():
    print("Updating users table...")

    with engine.begin() as conn:

        conn.execute(
            text("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS
                role VARCHAR(50)
                NOT NULL
                DEFAULT 'user'
            """)
        )

        conn.execute(
            text("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS
                organization VARCHAR(100)
            """)
        )

        conn.execute(
            text("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS
                is_staff BOOLEAN
                NOT NULL
                DEFAULT FALSE
            """)
        )

        conn.execute(
            text("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS
                is_active BOOLEAN
                NOT NULL
                DEFAULT TRUE
            """)
        )

    print("Staff authorization fields added successfully.")


if __name__ == "__main__":
    migrate()