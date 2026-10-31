from sqlalchemy import (
    Column, Integer, String, Float,
    Boolean, Text, ForeignKey, DateTime, func
)
from sqlalchemy.orm import relationship

from app.database import Base


class WantedCriminal(Base):
    __tablename__ = "wanted_criminals"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=True)
    nickname = Column(String, nullable=False)
    reward = Column(Float, nullable=False)

    last_coordinates = Column(String, nullable=True)
    last_location_note = Column(Text, nullable=True)

    difficulty = Column(Integer, nullable=False)

    armed = Column(Boolean, default=False)
    has_crew = Column(Boolean, default=False)
    escape_master = Column(Boolean, default=False)

    hunt_logs = relationship(
        "HuntLog",
        back_populates="criminal",
        cascade="all, delete-orphan"
    )


class HuntLog(Base):
    __tablename__ = "hunt_logs"

    id = Column(Integer, primary_key=True, index=True)

    criminal_id = Column(
        Integer,
        ForeignKey("wanted_criminals.id"),
        nullable=False
    )

    success = Column(Boolean, nullable=False)
    notes = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    criminal = relationship(
        "WantedCriminal",
        back_populates="hunt_logs"
    )