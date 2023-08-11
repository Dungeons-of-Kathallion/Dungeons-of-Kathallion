from colorama import Fore, Back, Style, deinit, init

init()

class Colors:
    
  def __init__(self):
    # Basic colors
    self.reset = Fore.RESET
    self.black = Fore.BLACK
    self.white = Fore.WHITE
    self.red = Fore.RED
    self.green = Fore.GREEN
    self.yellow = Fore.YELLOW
    self.blue = Fore.BLUE
    self.magenta = Fore.MAGENTA
    self.cyan = Fore.CYAN
    # Background colors
    self.back_reset = Back.RESET
    self.back_black = Back.BLACK
    self.back_white = Back.WHITE
    self.back_red = Back.RED
    self.back_green = Back.GREEN
    self.back_yellow = Back.YELLOW
    self.back_blue = Back.BLUE
    self.back_magenta = Back.MAGENTA
    self.back_cyan = Back.CYAN
    # Text styles
    self.style_normal = Style.NORMAL
    self.style_dim = Style.DIM
    self.style_bright = Style.BRIGHT

    self.reset_all = Style.RESET_ALL
      
deinit()
