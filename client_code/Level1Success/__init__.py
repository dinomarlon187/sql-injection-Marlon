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
      
    login_list = properties.get('login_list')
    login_state = login_list[0]
    if (login_list[1]):
      accNo = properties.get('AccountNo')
      if (accNo == None):
        login_state += ' But AccountNo was not passed.'
        anvil.server.session['login'] = True
      else:
        anvil.js.window.location.href+= "?AccountNo="+str(accNo)
        self.button_1.text = "Back"
        

    self.rich_text_1.content = login_state
    
      
    
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Level1')
