from database.database import SessionLocal
from database.schemas import UsageLogCreate
from database.crud import create_usage_log
from datetime import datetime
from zoneinfo import ZoneInfo

def log_usage(client_id: str, endpoint: str, size: int, is_successful: bool = True, error_message: str = None):
    db = SessionLocal()
    try:
        usage_log = UsageLogCreate(
            client_id=client_id,
            endpoint=endpoint,
            timestamp=datetime.now(ZoneInfo('Asia/Jakarta')),
            size=size,
            is_successful=is_successful,
            error_message=error_message
        )
        create_usage_log(db, usage_log)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()