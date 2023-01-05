from sqlalchemy import Column, select
from sqlalchemy import inspect
from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.engine import Inspector
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"
    # atributos
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname= {self.fullname})"


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String(40), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="address")

    def __repr__(self):
        return f"Address (id={self.id}, email_address={self.email_address})"


print(User.__tablename__)
print(Address.__table__)

#conexao com o database
engine = create_engine("sqlite://")

#criando as classes como tabelas no database
Base.metadata.create_all(engine)


inspetor = inspect(engine)
print(inspetor.has_table("user_account"))

print(inspetor.get_table_names())
print(inspetor.default_schema_name)

with Session(engine) as session:
    pedro = User(
        name='Pedro',
        fullname='Pedro Carneiro',
        address=[Address(email_address='pedrocarneirocunha87@gmail.com')]
    )

    sandy = User(
        name='sandy',
        fullname='Sandy Guedes',
        address=[Address(email_address='sandyguedes55@yahoo.com'),
               Address(email_address='sandyg23@gmail.com')]
    )

    patrick = User(
        name='patrick',
        fullname='Patrick Guedes',
        address=[Address(email_address='patrickguedes23@yahoo.com')]
    )

    # enviando para o database (persistencia de dados)
    session.add_all([pedro, sandy, patrick])

    session.commit()

#retorna o dado com o parametro fornecido
stmt = select(User).where(User.name.in_(["Pedro", "patrick"]))
print("Recuperando usuarios a partir de condicao de filtragem")
for user in session.scalars(stmt):
    print("\nQuery:")
    print(user)

stmt_address = select(Address).where(Address.user_id.in_([2]))
print("\nRecuperando enderecos de email de sandy")
for address in session.scalars(stmt_address):
    print(address)

print("\n")
print("Recuperando info de maneira ordenada")
stmt_order = select(User).order_by(User.fullname.desc())
for result in session.scalars(stmt_order):
    print(result)

print("\n")
stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)
for result in session.scalars(stmt_join):
    print(result)

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando statement a partir da connection")
for result in results:
    print(result)

