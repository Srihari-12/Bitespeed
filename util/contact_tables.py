from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from config.db import Base

class Contact(Base):
    __tablename__ = "Contact"

    id = Column(Integer, primary_key=True, index=True)
    phoneNumber = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    linkedId = Column(Integer, ForeignKey("Contact.id"), nullable=True)
    linkPrecedence = Column(Enum("primary", "secondary"), nullable=False)
    createdAt = Column(DateTime, server_default=func.now())
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deletedAt = Column(DateTime, nullable=True)
