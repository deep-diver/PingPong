from pingpong.pingpong import PromptFmt, UIFmt
from pingpong.pingpong import PPManager

class GradioChatUIFmt(UIFmt):
  @classmethod
  def ui(cls, pingpong):
    return (pingpong.ping, pingpong.pong)

class GradioChatPPManager(PPManager):
  def build_prompts(self, fmt: PromptFmt):
    results = ""

    for idx, pingpong in enumerate(self.pingpongs):
      results += fmt.prompt(pingpong)

      if idx != len(self.pingpongs)-1:
        results += """

"""

    return results

  def build_uis(self, fmt: UIFmt = GradioChatUIFmt):
    results = []

    for pingpong in self.pingpongs:
      results.append(fmt.ui(pingpong))

    return results