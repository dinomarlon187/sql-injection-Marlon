from ._anvil_designer import LevelTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Level(LevelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_login_click(self, **event_args):
    """This method is called when the button is clicked"""
    username = self.text_box_username.text
    password = self.text_box_password.text
    if self.check_box_injection.checked:
      login_state = anvil.server.call("Login_InjectionPosssible", password, username)
    else:
      login_state = anvil.server.call("Login_InjectionImpossible", password, username)
    open_form('user', login_state = login_state, AccountState = anvil.server.call('get_accountNo',username,password) )

