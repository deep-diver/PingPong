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
  def __init__(self, ctx: str=""):
    self.ctx = ctx
    self.pingpongs = []

  def add_pingpong(self, pingpong):
    self.pingpongs.append(pingpong)

  def pop_pingpong(self):
    return self.pingpongs.pop()

  def build_prompts(self, from_idx: int, fmt: PromptFmt):
    pass

  def build_uis(self, from_idx: int, fmt: UIFmt):
    pass
    