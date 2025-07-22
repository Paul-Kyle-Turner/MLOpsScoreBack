from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class State(Base):
    """SQLAlchemy model for application state storage."""
    __tablename__ = 'state'
    __table_args__ = {'schema': 'state'}
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    state = Column(String(512), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    def __repr__(self):
        return f"<State(id={self.id}, state='{self.state[:50]}...', created_at={self.created_at})>"
