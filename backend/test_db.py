from database import SessionLocal
from models import User, Request

def test_db_connection():
    """Test database connection and query"""
    try:
        db = SessionLocal()
        
        # Test query
        users = db.query(User).all()
        print(f"✅ Database connection successful!")
        print(f"✅ Found {len(users)} users in database")
        
        for user in users:
            print(f"  - {user.username} ({user.role}): {user.email}")
        
        db.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_db_connection()
