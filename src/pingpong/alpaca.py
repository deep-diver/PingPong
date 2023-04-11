from pingpong.pingpong import PromptFmt

class AlpacaPromptFmt(PromptFmt):
  @classmethod
  def prompt(cls, pingpong):
    return f"""### Instruction: {pingpong.ping}

### Response: {pingpong.pong}"""
