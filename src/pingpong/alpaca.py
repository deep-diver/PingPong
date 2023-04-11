from pingpong.pingpong import PPManager
from pingpong.pingpong import PromptFmt

class AlpacaPromptFmt(PromptFmt):
  @classmethod
  def prompt(cls, pingpong):
    return f"""### Instruction: {pingpong.ping}

### Response: {pingpong.pong}"""

class AlpacaChatPPManager(PPManager):
  def build_prompts(self, from_idx: int=0, fmt: PromptFmt=AlpacaPromptFmt):
    if self.ctx == "":
      results = ""
    else:
      results = f"""Input: {self.ctx}

"""

    for idx, pingpong in enumerate(self.pingpongs[from_idx:]):
      print(idx)
      results += fmt.prompt(pingpong)

      if idx != len(self.pingpongs[from_idx:])-1:
        results += """

"""

    return results