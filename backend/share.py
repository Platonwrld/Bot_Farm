import json

import pygsheets
from app_init import get_settings
from database.models import models
from sqlalchemy import inspect
from string import ascii_uppercase
from app_init import engine
from sqlalchemy.orm import Session

ga = pygsheets.authorize(service_file="google_key.json")

config = get_settings()
table = ga.open_by_url(config['google_sheets_table_link'])

table.share("danilnikitin9696@gmail.com", role="writer")