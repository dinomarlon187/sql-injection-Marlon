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
def Login_InjectionPosssible(password, username):
  conn = sqlite3.connect(data_files['database'])
  cursor = conn.cursor()
  query = f"SELECT username,isAdmin FROM Users WHERE username = '{username}' AND password = '{password}';"
  cursor.execute(query)
  result = cursor.fetchone()
  conn.close()
  if result == None:
    return f"Login Failed: {query}"
  else:
    return f"Login Successful: {query}"

@anvil.server.callable
def Login_InjectionImpossible(password, username):
  pattern = "[0-9A-Za-z]+$"
  if not re.match(pattern, username):
    return "Error: Username should only contain letters and numbers!"
  if not re.match(pattern, username):
    return "Error: Password should only contain letters and numbers!"
  anvil.server.call("Login_InjectionPosssible",password,username)
  



@anvil.server.callable
def get_accountNo(username, password):
  con = sqlite3.connect(data_files["database"])
  cur = con.cursor()
  print(username)
  query = "SELECT AccountNo FROM Users WHERE username = ? AND password = ?"
  cur.execute(query, (username, password))
  reslut = cur.fetchone()
  if reslut == None:
    return [False , ' ']
  else:
    return [True, reslut]
  con.close()


