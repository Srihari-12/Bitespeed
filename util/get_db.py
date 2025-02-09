from config.db import SessionLocal  # ✅ Ensure correct import from config

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

