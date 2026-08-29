
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}
)

class TestCustomerRepository:

    @pytest.fixture
    def session(self):
        SQLModel.metadata.create_all(test_engine)

        with Session(test_engine) as session:
            yield session

        SQLModel.metadata.drop_all(test_engine)

    @pytest.fixture
    def saved_customer(self, session) -> Customer:
        customer = Customer(
            name="John",
            email="john@gmail.com",
            password="test-password"
        )

        session.add(customer)
        session.commit()
        session.refresh(customer)

        return customer

    def test_save(self, session):
        repo = CustomerRepository(session)

        customer = Customer(
            name="John",
            email="john@gmail.com",
            password="test-password"
        )

        saved_customer = repo.save(customer)

        assert saved_customer.id is not None
        assert saved_customer.name == "John"
        assert saved_customer.email == "john@gmail.com"