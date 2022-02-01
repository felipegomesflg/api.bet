from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, text, REAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class BetOTW(Base):
    __tablename__ = 'bet_otw'

    id = Column(Integer, primary_key=True, server_default=text("nextval('bet_id_seq'::regclass)"))
    created_at = Column(DateTime(True), server_default=text("now()"))
    reference_date = Column(DateTime(True), server_default=text("now()"))
    bet_id = Column(ForeignKey('bet.id'), nullable=False)

    bet = relationship('Bet')
    

class Bet(Base):
    __tablename__ = 'bet'

    id = Column(Integer, primary_key=True, server_default=text("nextval('bet_id_seq'::regclass)"))
    title = Column(String, nullable=False)
    initial_value = Column(REAL)
    closure_value = Column(REAL)
    user_id = Column(ForeignKey('users.id'))
    created_at = Column(DateTime(True), server_default=text("now()"))
    updated_at = Column(DateTime(True), server_default=text("now()"))
    published = Column(Boolean, nullable=False, server_default=text("false"))

    user = relationship('User')



class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, server_default=text("nextval('review_id_seq'::regclass)"))
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    cod = Column(String, nullable=False)
    user_id = Column(ForeignKey('users.id'))
    created_at = Column(DateTime(True), server_default=text("now()"))
    updated_at = Column(DateTime(True), server_default=text("now()"))
        
    user = relationship('User')


class User(Base):
    __tablename__ = 'users'

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    company_name = Column(String)
    company_role = Column(String)
    avatar = Column(String)
    email = Column(String, primary_key=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String)
    about = Column(String)
    id = Column(Integer, primary_key=True, server_default=text("nextval('user_id_seq'::regclass)"))
    created_at = Column(DateTime(True), server_default=text("now()"))
    updated_at = Column(DateTime(True), server_default=text("now()"))


class BetComent(Base):
    __tablename__ = 'bet_coment'

    id = Column(Integer, primary_key=True, server_default=text("nextval('coment_id_seq'::regclass)"))
    message = Column(String, nullable=False)
    created_at = Column(DateTime(True), server_default=text("now()"))
    updated_at = Column(DateTime(True), server_default=text("now()"))
    bet_id = Column(ForeignKey('bet.id'), nullable=False)

    bet = relationship('Bet')


class BetItem(Base):
    __tablename__ = 'bet_item'

    id = Column(Integer, primary_key=True, server_default=text("nextval('bet_item_id_seq'::regclass)"))
    bet_id = Column(ForeignKey('bet.id'), nullable=False, index=True)
    cod = Column(String)
    quantity = Column(REAL)
    initial_unit_value = Column(REAL)
    closure_unit_value = Column(REAL)

    bet = relationship('Bet')


class BetLike(Base):
    __tablename__ = 'bet_like'

    id = Column(Integer, primary_key=True, server_default=text("nextval('bet_like_id_seq'::regclass)"))
    user_id = Column(ForeignKey('users.id'))
    bet_id = Column(ForeignKey('bet.id'), index=True)
    created_at = Column(DateTime(True), server_default=text("now()"))

    bet = relationship('Bet')
    user = relationship('User')


class ReviewComent(Base):
    __tablename__ = 'review_coment'

    id = Column(Integer, primary_key=True, server_default=text("nextval('review_coment_id_seq'::regclass)"))
    message = Column(String)
    created_at = Column(DateTime(True), server_default=text("now()"))
    updated_at = Column(DateTime(True), server_default=text("now()"))
    review_id = Column(ForeignKey('review.id'))
    user_id = Column(ForeignKey('users.id'))

    review = relationship('Review')
    user = relationship('User')


class ReviewLike(Base):
    __tablename__ = 'review_like'

    id = Column(Integer, primary_key=True, server_default=text("nextval('review_like_id_seq'::regclass)"))
    user_id = Column(ForeignKey('users.id'))
    review_id = Column(ForeignKey('review.id'))
    created_at = Column(DateTime(True), server_default=text("now()"))

    review = relationship('Review')
    user = relationship('User')


class UserFavBet(Base):
    __tablename__ = 'user_fav_bet'

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"userFavBet_id_seq\"'::regclass)"))
    user_id = Column(ForeignKey('users.id'))
    bet_id = Column(ForeignKey('bet.id'))
    created_at = Column(DateTime(True), server_default=text("now()"))

    bet = relationship('Bet')
    user = relationship('User')


class UserFavCod(Base):
    __tablename__ = 'user_fav_cod'

    id = Column(Integer, primary_key=True, server_default=text("nextval('user_fav_cod_id_seq'::regclass)"))
    user_id = Column(ForeignKey('users.id'))
    cod = Column(String)
    created_at = Column(DateTime(True), server_default=text("now()"))

    user = relationship('User')


class UserFavUser(Base):
    __tablename__ = 'user_fav_user'

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"userFavUser_id_seq\"'::regclass)"))
    user_id = Column(ForeignKey('users.id'))
    user_fav_id = Column(ForeignKey('users.id'))
    created_at = Column(DateTime(True), server_default=text("now()"))

    user = relationship('User', primaryjoin='UserFavUser.user_fav_id == User.id')
    user1 = relationship('User', primaryjoin='UserFavUser.user_id == User.id')


class BetComentLike(Base):
    __tablename__ = 'bet_coment_like'

    id = Column(Integer, primary_key=True, server_default=text("nextval('bet_coment_like_id_seq'::regclass)"))
    user_id = Column(ForeignKey('users.id'), nullable=False)
    bet_coment_id = Column(ForeignKey('bet_coment.id'), nullable=False)
    created_at = Column(DateTime(True), server_default=text("now()"))

    bet_coment = relationship('BetComent')
    user = relationship('User')


class ReviewComentLike(Base):
    __tablename__ = 'review_coment_like'

    id = Column(Integer, primary_key=True, server_default=text("nextval('review_coment_like_id_seq'::regclass)"))
    user_id = Column(ForeignKey('users.id'))
    review_coment_id = Column(ForeignKey('review_coment.id'))
    created_at = Column(DateTime(True), server_default=text("now()"))

    review_coment = relationship('ReviewComent')
    user = relationship('User')

class Ticker(Base):
    __tablename__ = 'ticker'

    id = Column(Integer, primary_key=True, server_default=text("nextval('coment_id_seq'::regclass)"))
    symbol = Column(String, nullable=False)
    name = Column(String, nullable=False)
    setor = Column(String)
    tipo = Column(String)
    site = Column(String)
    created_at = Column(DateTime(True), server_default=text("now()"))
    updated_at = Column(DateTime(True), server_default=text("now()"))