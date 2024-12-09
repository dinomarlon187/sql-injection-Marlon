import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3
import hashlib
import re



@anvil.server.callable
def Login(password, username, possible):
  if not possible:
    pattern = "[0-9A-Za-z]+$"
    if not re.match(pattern, username):
      return ["Error: Username should only contain letters and numbers!",False]
    if not re.match(pattern, username):
      return ["Error: Password should only contain letters and numbers!", False]
  conn = sqlite3.connect(data_files['database'])
  cursor = conn.cursor()
  query = f"SELECT username,isAdmin FROM Users WHERE username = '{username}' AND password = '{password}';"
  res = list(cursor.execute(query))

  conn.close()
  if len(res) == 0:
    return [f"Login Failed: {query}", False]
  else:
    return [f"Login Successful: {query}", True]


  



@anvil.server.callable
def get_accountNo(username, password):
  con = sqlite3.connect(data_files["database"])
  cursor = con.cursor()
  query = "SELECT AccountNo FROM Users WHERE username = ? AND password = ?"
  res = list(cursor.execute(query, (username, password)))
  con.close()
  if len(res) == 0:
    return None
  else:
    return res[0]


