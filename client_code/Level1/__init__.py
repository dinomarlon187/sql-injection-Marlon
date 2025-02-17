from ._anvil_designer import Level1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Level1(Level1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if anvil.server.call('IsLoggedIn'):
      open_form('Level1Success')
    else:
      set_url_hash()

      
       

    # Any code you write here will run before the form opens.

  def button_login_click(self, **event_args):
    """This method is called when the button is clicked"""
    username = self.text_box_username.text
    password = self.text_box_password.text
    login_state = anvil.server.call("Login", password, username, self.check_box_injection.checked)
    self.label_message.text = login_state[0]
    if login_state[1]:
      res = anvil.server.call('get_accountNo',username,password)
      if res != None:
        set_url_hash(f'?AccountNo={res}')
      open_form('Level1Success')
      
      
      

    

