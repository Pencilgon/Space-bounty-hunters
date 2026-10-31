from app.database import SessionLocal, Base, engine
from app.models import WantedCriminal, HuntLog

Base.metadata.create_all(bind=engine)

db = SessionLocal()

criminals = [
    WantedCriminal(
        name="Unknown",
        nickname="Void Reaper",
        reward=150000,
        last_coordinates="45.123, 67.456",
        last_location_note="Last seen near Mars",
        difficulty=9,
        armed=True,
        has_crew=True,
        escape_master=True
    ),
    WantedCriminal(
        name="John Carter",
        nickname="Star Thief",
        reward=50000,
        last_coordinates="20.456, 30.789",
        last_location_note="Abandoned space station",
        difficulty=6,
        armed=True,
        has_crew=False,
        escape_master=True
    ),
    WantedCriminal(
        name="Sarah Connor",
        nickname="Nebula Ghost",
        reward=85000,
        last_coordinates="12.345, 56.789",
        last_location_note="Near Jupiter",
        difficulty=8,
        armed=False,
        has_crew=True,
        escape_master=True
    ),
    WantedCriminal(
        name="Unknown",
        nickname="Asteroid King",
        reward=25000,
        last_coordinates=None,
        last_location_note="Somewhere in the asteroid belt",
        difficulty=4,
        armed=True,
        has_crew=False,
        escape_master=False
    ),
    WantedCriminal(
        name="Alex Morgan",
        nickname="Space Bandit",
        reward=10000,
        last_coordinates="10.111, 20.222",
        last_location_note="Last seen on Europa",
        difficulty=3,
        armed=False,
        has_crew=False,
        escape_master=False
    )
]

try:
    db.add_all(criminals)
    db.commit()

    db.refresh(criminals[0])
    db.refresh(criminals[1])
    db.refresh(criminals[2])
    db.refresh(criminals[3])
    db.refresh(criminals[4])

    logs = [
        HuntLog(criminal_id=criminals[0].id, success=False, notes="Target escaped."),
        HuntLog(criminal_id=criminals[0].id, success=False, notes="Lost in asteroid field."),
        HuntLog(criminal_id=criminals[1].id, success=True, notes="Captured near station."),
        HuntLog(criminal_id=criminals[1].id, success=False, notes="Failed ambush."),
        HuntLog(criminal_id=criminals[2].id, success=False, notes="Target disappeared."),
        HuntLog(criminal_id=criminals[2].id, success=True, notes="Captured by surprise."),
        HuntLog(criminal_id=criminals[3].id, success=True, notes="Target surrendered."),
        HuntLog(criminal_id=criminals[3].id, success=False, notes="Ship destroyed, target escaped."),
        HuntLog(criminal_id=criminals[4].id, success=True, notes="Captured on Europa."),
        HuntLog(criminal_id=criminals[4].id, success=False, notes="Initial tracking failed.")
    ]

    db.add_all(logs)
    db.commit()

    print("Database populated successfully!")

finally:
    db.close()