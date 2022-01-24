from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, text, REAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class BetOTW(Base):
    __tablename__ = 'bet_otw'

    id = Column(Integer, primary_key=True, server_default=text("nextval('bet_id_seq'::regclass)"))
    createdAt = Column(DateTime(True), server_default=text("now()"))
    referenceDate = Column(DateTime(True), server_default=text("now()"))
    betId = Column(ForeignKey('bet.id'), nullable=False)

    bet = relationship('Bet')
    

class Bet(Base):
    __tablename__ = 'bet'

    id = Column(Integer, primary_key=True, server_default=text("nextval('bet_id_seq'::regclass)"))
    title = Column(String, nullable=False)
    initialValue = Column(REAL)
    closureValue = Column(REAL)
    createdAt = Column(DateTime(True), server_default=text("now()"))
    updatedAt = Column(DateTime(True), server_default=text("now()"))
    published = Column(Boolean, nullable=False, server_default=text("false"))


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, server_default=text("nextval('review_id_seq'::regclass)"))
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    cod = Column(String, nullable=False)
    createdAt = Column(DateTime(True), server_default=text("now()"))
    updatedAt = Column(DateTime(True), server_default=text("now()"))


class User(Base):
    __tablename__ = 'users'

    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    companyName = Column(String)
    companyRole = Column(String)
    avatar = Column(String)
    email = Column(String, primary_key=True, nullable=False)
    password = Column(String, nullable=False)
    telefone = Column(String)
    id = Column(Integer, primary_key=True, server_default=text("nextval('user_id_seq'::regclass)"))
    createdAt = Column(DateTime(True), server_default=text("now()"))
    updatedAt = Column(DateTime(True), server_default=text("now()"))


class BetComent(Base):
    __tablename__ = 'bet_coment'

    id = Column(Integer, primary_key=True, server_default=text("nextval('coment_id_seq'::regclass)"))
    message = Column(String, nullable=False)
    createdAt = Column(DateTime(True), server_default=text("now()"))
    updatedAt = Column(DateTime(True), server_default=text("now()"))
    betId = Column(ForeignKey('bet.id'), nullable=False)

    bet = relationship('Bet')


class BetItem(Base):
    __tablename__ = 'bet_item'

    id = Column(Integer, primary_key=True, server_default=text("nextval('bet_item_id_seq'::regclass)"))
    betId = Column(ForeignKey('bet.id'), nullable=False, index=True)
    cod = Column(String)
    quantity = Column(REAL)
    initialUnitValue = Column(REAL)
    closureUnitValue = Column(REAL)

    bet = relationship('Bet')


class BetLike(Base):
    __tablename__ = 'bet_like'

    id = Column(Integer, primary_key=True, server_default=text("nextval('bet_like_id_seq'::regclass)"))
    userId = Column(ForeignKey('users.id'))
    betId = Column(ForeignKey('bet.id'), index=True)
    createdAt = Column(DateTime(True), server_default=text("now()"))

    bet = relationship('Bet')
    user = relationship('User')


class ReviewComent(Base):
    __tablename__ = 'review_coment'

    id = Column(Integer, primary_key=True, server_default=text("nextval('review_coment_id_seq'::regclass)"))
    message = Column(String)
    createdAt = Column(DateTime(True), server_default=text("now()"))
    updatedAt = Column(DateTime(True), server_default=text("now()"))
    reviewId = Column(ForeignKey('review.id'))
    userId = Column(ForeignKey('users.id'))

    review = relationship('Review')
    user = relationship('User')


class ReviewLike(Base):
    __tablename__ = 'review_like'

    id = Column(Integer, primary_key=True, server_default=text("nextval('review_like_id_seq'::regclass)"))
    userId = Column(ForeignKey('users.id'))
    reviewId = Column(ForeignKey('review.id'))
    createdAt = Column(DateTime(True), server_default=text("now()"))

    review = relationship('Review')
    user = relationship('User')


class UserFavBet(Base):
    __tablename__ = 'user_fav_bet'

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"userFavBet_id_seq\"'::regclass)"))
    userId = Column(ForeignKey('users.id'))
    betId = Column(ForeignKey('bet.id'))
    createdAt = Column(DateTime(True), server_default=text("now()"))

    bet = relationship('Bet')
    user = relationship('User')


class UserFavCod(Base):
    __tablename__ = 'user_fav_cod'

    id = Column(Integer, primary_key=True, server_default=text("nextval('user_fav_cod_id_seq'::regclass)"))
    userId = Column(ForeignKey('users.id'))
    cod = Column(String)
    createdAt = Column(DateTime(True), server_default=text("now()"))

    user = relationship('User')


class UserFavUser(Base):
    __tablename__ = 'user_fav_user'

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"userFavUser_id_seq\"'::regclass)"))
    userId = Column(ForeignKey('users.id'))
    userFavId = Column(ForeignKey('users.id'))
    createdAt = Column(DateTime(True), server_default=text("now()"))

    user = relationship('User', primaryjoin='UserFavUser.userFavId == User.id')
    user1 = relationship('User', primaryjoin='UserFavUser.userId == User.id')


class BetComentLike(Base):
    __tablename__ = 'bet_coment_like'

    id = Column(Integer, primary_key=True, server_default=text("nextval('bet_coment_like_id_seq'::regclass)"))
    userId = Column(ForeignKey('users.id'), nullable=False)
    betComentId = Column(ForeignKey('bet_coment.id'), nullable=False)
    createdAt = Column(DateTime(True), server_default=text("now()"))

    bet_coment = relationship('BetComent')
    user = relationship('User')


class ReviewComentLike(Base):
    __tablename__ = 'review_coment_like'

    id = Column(Integer, primary_key=True, server_default=text("nextval('review_coment_like_id_seq'::regclass)"))
    userId = Column(ForeignKey('users.id'))
    reviewComentId = Column(ForeignKey('review_coment.id'))
    createdAt = Column(DateTime(True), server_default=text("now()"))

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
    createdAt = Column(DateTime(True), server_default=text("now()"))
    updatedAt = Column(DateTime(True), server_default=text("now()"))