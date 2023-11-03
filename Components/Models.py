from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Gender(Base):
    __tablename__ = 'gender'
    id = Column(Integer, primary_key=True)
    gender_type = Column(String(10), unique=True, nullable=False)


class CustomerType(Base):
    __tablename__ = 'customer_type'
    id = Column(Integer, primary_key=True)
    type = Column(String(50), unique=True, nullable=False)


class TypeOfTravel(Base):
    __tablename__ = 'type_of_travel'
    id = Column(Integer, primary_key=True)
    travel_type = Column(String(50), unique=True, nullable=False)


class Class(Base):
    __tablename__ = 'class'
    id = Column(Integer, primary_key=True)
    class_type = Column(String(50), unique=True, nullable=False)


class Satisfaction(Base):
    __tablename__ = 'satisfaction'
    id = Column(Integer, primary_key=True)
    satisfaction_level = Column(String(50), unique=True, nullable=False)


class Age(Base):
    __tablename__ = 'age'
    id = Column(Integer, primary_key=True)
    age = Column(Integer, unique=True, nullable=False)


class SatisfactionCustomer(Base):
    __tablename__ = 'satisfaction_customers'
    id = Column(Integer, primary_key=True)
    gender_id = Column(Integer, ForeignKey('gender.id'))
    customer_type_id = Column(Integer, ForeignKey('customer_type.id'))
    type_of_travel_id = Column(Integer, ForeignKey('type_of_travel.id'))
    class_id = Column(Integer, ForeignKey('class.id'))
    satisfaction_id = Column(Integer, ForeignKey('satisfaction.id'))
    age_id = Column(Integer, ForeignKey('age.id'))
    flight_distance = Column(Float, nullable=True)
    inflight_wifi_service = Column(Integer, nullable=True)
    departure_arrival_time_convenient = Column(Integer, nullable=True)
    ease_of_online_booking = Column(Integer, nullable=True)
    gate_location = Column(Integer, nullable=True)
    food_and_drink = Column(Integer, nullable=True)
    online_boarding = Column(Integer, nullable=True)
    seat_comfort = Column(Integer, nullable=True)
    inflight_entertainment = Column(Integer, nullable=True)
    on_board_service = Column(Integer, nullable=True)
    leg_room_service = Column(Integer, nullable=True)
    baggage_handling = Column(Integer, nullable=True)
    checkin_service = Column(Integer, nullable=True)
    inflight_service = Column(Integer, nullable=True)
    cleanliness = Column(Integer, nullable=True)
    departure_delay_in_minutes = Column(Integer, nullable=True)
    arrival_delay_in_minutes = Column(Integer, nullable=True)

    gender_rel = relationship('Gender')
    customer_type = relationship('CustomerType')
    type_of_travel = relationship('TypeOfTravel')
    class_air = relationship('Class')
    satisfaction = relationship('Satisfaction')
    age = relationship('Age')
