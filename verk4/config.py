import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456'
    API_KEY = '5ca684664916f8654ef6ef3ed503d6a1'
    API_READ_ACCESS_TOKEN = 'eyJh...P9sB1Xldg'
