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
  def build_prompts(self, from_idx: int=0, to_idx: int=-1, fmt: PromptFmt=AlpacaPromptFmt):
    if to_idx == -1 or to_idx >= len(self.pingpongs):
      to_idx = len(self.pingpongs)

    results = fmt.ctx(self.ctx)

    for idx, pingpong in enumerate(self.pingpongs[from_idx:to_idx]):
      print(idx)
      results += fmt.prompt(pingpong)

      if from_idx+idx != to_idx-1:
        results += """

"""

    return results