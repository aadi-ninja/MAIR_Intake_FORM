from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/mair_db")

try:
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        result = connection.execute(text("SELECT COUNT(*) as user_count FROM users"))
        count = result.scalar()
        print(f"✅ Database connection successful!")
        print(f"✅ Found {count} users in database")
        
        # Get user details
        result = connection.execute(text("SELECT username, role, email FROM users"))
        print("\nUsers:")
        for row in result:
            print(f"  - {row[0]} ({row[1]}): {row[2]}")
            
except Exception as e:
    print(f"❌ Connection failed: {e}")
