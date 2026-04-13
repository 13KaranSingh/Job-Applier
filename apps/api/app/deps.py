from collections.abc import Generator

from packages.db.session import SessionLocal


def get_db() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

