import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://inventorydb:Inv3ntory#DB!2025@localhost/inventorydb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
