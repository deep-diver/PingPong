from pingpong.pingpong import PromptFmt, UIFmt
from pingpong.pingpong import PPManager
from pingpong.alpaca import AlpacaPromptFmt

class GradioChatUIFmt(UIFmt):
  @classmethod
  def ui(cls, pingpong):
    return (pingpong.ping, pingpong.pong)

class GradioChatPPManager(PPManager):
  def build_uis(self, from_idx: int=0, fmt: UIFmt=GradioChatUIFmt):
    results = []

    for pingpong in self.pingpongs[from_idx:]:
      results.append(fmt.ui(pingpong))

    return results

class GradioAlpacaChatPPManager(GradioChatPPManager):
  def build_prompts(self, from_idx: int=0, fmt: PromptFmt=AlpacaPromptFmt):
    results = ""

    for idx, pingpong in enumerate(self.pingpongs[from_idx:]):
      print(idx)
      results += fmt.prompt(pingpong)

      if idx != len(self.pingpongs[from_idx:])-1:
        results += """

"""

    return results