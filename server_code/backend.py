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
  cursor = con.cursor()
  query = f"SELECT Users.username, Balances.balance FROM Users INNER JOIN Balances ON Users.AccountNo = Balances.AccountNo WHERE Users.AccountNo = {id};"
  res = list(cursor.execute(query))
  try:
    hallo = res[0][0]
    return [True,hallo,res[0][1]]
  except:
    return [False,'No account matching the AccountNumber.']
    

