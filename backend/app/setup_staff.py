from backend.app.database.database import engine
from sqlalchemy import text

EMAIL = "phantomtest@example.com"

with engine.begin() as conn:
    result = conn.execute(
        text("""
            UPDATE users
            SET
                is_staff = TRUE,
                role = 'admin',
                organization = 'PhantomAI Development'
            WHERE email = :email
        """),
        {"email": EMAIL}
    )

    if result.rowcount == 0:
        print(f"❌ User not found: {EMAIL}")
    else:
        print(f"✅ Staff authorization configured for: {EMAIL}")
        print("   is_staff = TRUE")
        print("   role = admin")
        print("   organization = PhantomAI Development")
