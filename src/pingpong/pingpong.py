class PingPong:
  def __init__(self, ping, pong):
    self.ping = ping
    self.pong = pong

class PromptFmt:
  @classmethod
  def prompt(cls, pingpong):
    pass

class UIFmt:
  @classmethod
  def ui(cls, pingpong):
    pass

class PPManager:
  def __init__(self):
    self.pingpongs = []

  def add_pingpong(self, pingpong):
    self.pingpongs.append(pingpong)

  def pop_pingpong(self):
    return self.pingpongs.pop()

  def build_prompts(self, fmt: PromptFmt):
    pass

  def build_uis(self, fmt: UIFmt):
    pass
    