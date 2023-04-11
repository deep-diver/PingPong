from pingpong.pingpong import PromptFmt, UIFmt
from pingpong.alpaca import AlpacaPromptFmt, AlpacaChatPPManager

class GradioChatUIFmt(UIFmt):
  @classmethod
  def ui(cls, pingpong):
    return (pingpong.ping, pingpong.pong)

class GradioAlpacaChatPPManager(AlpacaChatPPManager):
  def build_uis(self, from_idx: int=0, fmt: UIFmt=GradioChatUIFmt):
    results = []

    for pingpong in self.pingpongs[from_idx:]:
      results.append(fmt.ui(pingpong))

    return results