# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class Devices(db.Model):

    __tablename__ = 'Devices'

    id = db.Column(db.Integer, primary_key=True)

    #__Devices_FIELDS__
    hostname = db.Column(db.String(255),  nullable=True)
    model = db.Column(db.String(255),  nullable=True)
    firmware_version = db.Column(db.String(255),  nullable=True)
    serial_number = db.Column(db.String(255),  nullable=True)
    location = db.Column(db.String(255),  nullable=True)

    #__Devices_FIELDS__END

    def __init__(self, **kwargs):
        super(Devices, self).__init__(**kwargs)


class Configs(db.Model):

    __tablename__ = 'Configs'

    id = db.Column(db.Integer, primary_key=True)

    #__Configs_FIELDS__
    config_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    #__Configs_FIELDS__END

    def __init__(self, **kwargs):
        super(Configs, self).__init__(**kwargs)


class Firewall_Policies(db.Model):

    __tablename__ = 'Firewall_Policies'

    id = db.Column(db.Integer, primary_key=True)

    #__Firewall_Policies_FIELDS__
    policy_name = db.Column(db.String(255),  nullable=True)
    src_interface = db.Column(db.String(255),  nullable=True)
    dst_interface = db.Column(db.String(255),  nullable=True)
    src_address = db.Column(db.String(255),  nullable=True)
    dst_address = db.Column(db.String(255),  nullable=True)
    service = db.Column(db.String(255),  nullable=True)
    action = db.Column(db.String(255),  nullable=True)
    status = db.Column(db.Boolean, nullable=True)

    #__Firewall_Policies_FIELDS__END

    def __init__(self, **kwargs):
        super(Firewall_Policies, self).__init__(**kwargs)



#__MODELS__END
