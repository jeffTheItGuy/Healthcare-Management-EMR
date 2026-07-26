import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("POSTGRES_DB", "test_db")

from app.database import Base, get_db
from app.main import app
from app.core.security import get_password_hash, create_access_token
from app.models.staff import Staff, StaffCredential, Department


# Use SQLite for unit tests; for pgvector tests use TEST_DATABASE_URL with Postgres
SQLALCHEMY_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "sqlite:///:memory:",
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


@pytest.fixture(scope="function")
def test_department(db):
    dept = Department(
        department_code="EMRG",
        department_name="Emergency",
        department_type="CLINICAL",
    )
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept


@pytest.fixture(scope="function")
def test_staff(db, test_department):
    staff = Staff(
        staff_number="S-001",
        national_id="63-1234567-A-12",
        first_name="Test",
        last_name="Doctor",
        role="DOCTOR",
        department_id=test_department.department_id,
        is_active=True,
    )
    db.add(staff)
    db.flush()

    cred = StaffCredential(
        staff_id=staff.staff_id,
        username="testdoc",
        password_hash=get_password_hash("password123"),
    )
    db.add(cred)
    db.commit()
    db.refresh(staff)
    return staff


@pytest.fixture(scope="function")
def auth_headers(test_staff):
    token = create_access_token(
        data={"sub": str(test_staff.staff_id), "role": test_staff.role}
    )
    return {"Authorization": f"Bearer {token}"}