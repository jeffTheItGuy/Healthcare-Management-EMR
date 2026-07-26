from sqlalchemy import Column, BigInteger, String, Text, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    log_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True))
    staff_id = Column(UUID(as_uuid=True))
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50))
    entity_id = Column(UUID(as_uuid=True))
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    session_id = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())