from pingpong.pingpong import PPManager
from pingpong.pingpong import PromptFmt

class AlpacaPromptFmt(PromptFmt):
  @classmethod
  def ctx(cls, context):
    if context is None or context == "":
      return ""
    else:
      return f"""### Input: {context}

"""

  @classmethod
  def prompt(cls, pingpong):
    return f"""### Instruction: {pingpong.ping}

### Response: {pingpong.pong}"""

class AlpacaChatPPManager(PPManager):
  def build_prompts(self, from_idx: int=0, fmt: PromptFmt=AlpacaPromptFmt):
    results = fmt.ctx(self.ctx)

    for idx, pingpong in enumerate(self.pingpongs[from_idx:]):
      print(idx)
      results += fmt.prompt(pingpong)

      if idx != len(self.pingpongs[from_idx:])-1:
        results += """

"""

    return results