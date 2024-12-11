from ._anvil_designer import Level1SuccessTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Level1Success(Level1SuccessTemplate):
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.url = anvil.js.window.location.href
    self.accNo = anvil.server.call('get_accountNumber_from_query',self.url)
    if (self.accNo == None):
      self.rich_text_1.content = "Login Successful but AccountNo was not passed."
    else:
      res = anvil.server.call('get_username_from_id', self.accNo)
      if res[0]:
        self.username = res[1]
        self.balance = res[2]
        self.rich_text_1.content = f"Welcome {self.username}. Your balance is {self.balance}."
      else:
        self.rich_text_1.content = res[1]
      
    
    
    
    
      
    
    # Any code you write here will run before the form opens.

  
