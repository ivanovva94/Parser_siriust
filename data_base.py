from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, create_engine, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///siriust.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    mail = Column(String(255), nullable=False)
    city = Column(String(255))
    wishlist_items = relationship("Wishlist", back_populates="user")

    __table_args__ = (
        UniqueConstraint('mail'),
    )


class Wishlist(Base):
    __tablename__ = "wishlists"
    id = Column(Integer(), primary_key=True)
    item_name = Column(Text(), nullable=False)
    retail_price = Column(Float(), nullable=False)
    trade_price = Column(Float(), nullable=False)
    reviews_count = Column(String(255), nullable=False)
    rating = Column(Float(), nullable=False)
    count_of_shops = Column(Integer(), nullable=False)
    reviews = Column(Text(), nullable=False)
    user_id = Column(Integer(), ForeignKey("users.id"))
    user = relationship("User", back_populates="wishlist_items")

    __table_args__ = (
        UniqueConstraint("user_id", "item_name", name="_user_items_un"),
    )


Base.metadata.create_all(engine)


def remove_user_wishlist(user_data):
    session = Session()
    user = session.query(User).filter(User.mail == user_data["mail"]).first()

    session.query(Wishlist).filter_by(user_id=user.id).delete()
    session.commit()
    session.close()


def add_user_data(user_data):
    try:
        session = Session()
        user = User(**user_data)

        session.add(user)
        session.commit()
        session.close()
        return True
    except IntegrityError:
        print(f'Пользователь {user_data["mail"]} уже существует!')
        print("Данные будут перезаписаны.")
        remove_user_wishlist(user_data)



def add_wishlist(mail, wishlist_data):
    session = Session()
    user = session.query(User).filter(User.mail == mail).first()

    wishlist = Wishlist(**wishlist_data)
    user.wishlist_items.append(wishlist)

    session.add(user)
    session.commit()
    session.close()


def display_data():
    session = Session()

    users = session.query(User).all()
    for user in users:
        print(f"User ID: {user.id}")
        print(f"Имя: {user.first_name}")
        print(f"Фамилия: {user.last_name}")
        print(f"Email: {user.mail}")
        print(f"Город: {user.city}")
        print("Избранные товары:")
        for wishlist_item in user.wishlist_items:
            print(f"- Название: {wishlist_item.item_name}")
            print(f"  Розничная цена: {wishlist_item.retail_price}")
            print(f"  Оптовая цена: {wishlist_item.trade_price}")
            print(f"  Количество отзывов: {wishlist_item.reviews_count}")
            print(f"  Рейтинг: {wishlist_item.rating}")
            print(f"  Количество магазинов, где есть товар: {wishlist_item.count_of_shops}")
            print(f"  Отзывы: {wishlist_item.reviews}")
            print()

    session.close()
