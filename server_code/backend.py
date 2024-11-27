import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3
import hashlib




def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


