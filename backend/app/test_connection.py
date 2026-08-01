from backend.app.database.database import engine

try:
    with engine.connect() as connection:
        print("✅ Successfully connected to PostgreSQL!")
except Exception as e:
    print("❌ Connection failed")
    print(e)