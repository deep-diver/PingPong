from pingpong.pingpong import PPManager
from pingpong.pingpong import PromptFmt, UIFmt

def build_prompts(
		ppm: PPManager=None, 
		from_idx: int=0, 
		to_idx: int=-1, 
		fmt: PromptFmt=None, 
		truncate_size: int=None
):
	if to_idx == -1 or to_idx >= len(ppm.pingpongs):
			to_idx = len(ppm.pingpongs)

	results = fmt.ctx(ppm.ctx)

	for idx, pingpong in enumerate(ppm.pingpongs[from_idx:to_idx]):
			results += fmt.prompt(pingpong, truncate_size=truncate_size)

	return results

def gradio_build_uis(
		ppm: PPManager=None, 
		from_idx: int=0, 
		to_idx: int=-1, 
		fmt: UIFmt=None
):
	if to_idx == -1 or to_idx >= len(ppm.pingpongs):
			to_idx = len(ppm.pingpongs)
	
	results = []
	
	for pingpong in ppm.pingpongs[from_idx:to_idx]:
			results.append(fmt.ui(pingpong))
			
	return results