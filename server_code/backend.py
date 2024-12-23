import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3
import hashlib
import re
import urllib.parse



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
    anvil.server.session["login"] = True
    anvil.server.session['accNo'] = anvil.server.call('get_accountNo',username,password)
    return ["", True]

@anvil.server.callable
def IsLoggedIn():
  if ('login' in anvil.server.session):
    return anvil.server.session['login']
  else:
    anvil.server.session['login'] = False
    return anvil.server.session['login']

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
    return res[0][0]
@anvil.server.callable
def get_accountNumber_from_query(url):
    query_string = url.split('?')[-1] if '?' in url else ''
    if query_string:
      query_params = urllib.parse.parse_qs(query_string)
      if "AccountNo" in query_params:
        return query_params["AccountNo"][0]
    return None
@anvil.server.callable
def get_accountNumber_from_session():
  return anvil.server.session['accNo']
  
@anvil.server.callable
def get_balance(id):
  con = sqlite3.connect(data_files["database"])
  cursor = con.cursor()
  query = "SELECT balance FROM Balances WHERE AccountNo = ?"
  res = list(cursor.execute(query, (id,)))
  return res[0][0]

@anvil.server.callable
def get_username_from_id(id):
  con = sqlite3.connect(data_files["database"])
  cur = con.cursor()
  
  query_balance = f"SELECT balance FROM Balances WHERE AccountNo = {id}"
  query_user = f"SELECT username FROM Users WHERE AccountNo = {id}"
  
  try:
      balance = cur.execute(query_balance).fetchall()
      user = cur.execute(query_user).fetchall()
      
  except Exception as e:
      return f"User not found.<br>{query_user}<br>{query_balance}<br>{e}"

  user = [u[0] for u in user if isinstance(u, tuple)]
  balance = [b[0] for b in balance if isinstance(b, tuple)]
  user = user[0] if len(user) == 1 else user
  balance = balance[0] if len(balance) == 1 else balance

  if user:
      return f"Welcome {user}! Your balance is {balance}."
  else:
      return f"User not found.<br>{query_user}<br>{query_balance}"
    


@anvil.server.callable
def del_session():
  anvil.server.session["login"] = False