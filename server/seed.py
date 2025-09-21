# seed.py
from app import app, db
from models import Chama, Member, Contribution
from datetime import datetime

with app.app_context():
    # Clear existing data
    Contribution.query.delete()
    Member.query.delete()
    Chama.query.delete()
    db.session.commit()

    # -------------------------------
    # CREATE CHAMAS
    # -------------------------------
    chama1 = Chama(name="Investors Club", description="Real estate investments")
    chama2 = Chama(name="Tech Savers", description="Tech-focused savings group")

    db.session.add_all([chama1, chama2])
    db.session.commit()

    # -------------------------------
    # CREATE MEMBERS
    # -------------------------------
    # No chama_id or chama here (since model doesn't support it)
    member1 = Member(name="Alice", email="alice@example.com")
    member2 = Member(name="Bob", email="bob@example.com")
    member3 = Member(name="Charlie", email="charlie@example.com")

    db.session.add_all([member1, member2, member3])
    db.session.commit()

    # -------------------------------
    # CREATE CONTRIBUTIONS
    # -------------------------------
    # Link Members <-> Chamas via Contribution table (bridge)
    c1 = Contribution(
        amount=5000,
        date=datetime.utcnow(),
        member_id=member1.id,   # link with IDs
        chama_id=chama1.id
    )
    c2 = Contribution(
        amount=3000,
        date=datetime.utcnow(),
        member_id=member2.id,
        chama_id=chama1.id
    )
    c3 = Contribution(
        amount=7000,
        date=datetime.utcnow(),
        member_id=member3.id,
        chama_id=chama2.id
    )

    db.session.add_all([c1, c2, c3])
    db.session.commit()

    print("Database seeded successfully!")
