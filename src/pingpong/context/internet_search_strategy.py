import re
import copy
import json
import random
import string
import http.client

import chromadb
import torch
import torch.nn.functional as F

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModel

from pingpong import PingPong
from pingpong.pingpong import PPManager
from pingpong.context.strategy import CtxStrategy

default_instruction = """Based on the provided texts below, please answer to '{ping}' in your own words. Try to explain in detailed introduction, body, and conclusion structure as much as possible.
=====================
"""

class SimilaritySearcher:
    def __init__(
        self, model, tokenizer, max_length=512, device="cpu"
    ):
        self.model = model
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.device = device

    def get_embeddings(self, input_texts):
        # Tokenize the input texts
        batch_dict = self.tokenizer(
            input_texts,
            max_length=self.max_length,
            padding=True,
            truncation=True,
            return_tensors='pt'
        ).to(self.device)

        outputs = self.model(**batch_dict)
        embeddings = self._average_pool(
            outputs.last_hidden_state, batch_dict['attention_mask']
        )

        embeddings = F.normalize(embeddings, p=2, dim=1)
        
        embeddings_cpu = embeddings.to("cpu")
        embeddings_list = embeddings_cpu.tolist()
        
        if self.device == "cuda":
            del embeddings

            torch.cuda.empty_cache()        
        
        return embeddings_cpu, embeddings_list
    
    def _average_pool(
        self,
        last_hidden_states,
        attention_mask
    ):
        last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
        return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

    @classmethod
    def from_pretrained(cls, base_name="intfloat/e5-large-v2", max_length=512, device="cpu"):
        tokenizer = AutoTokenizer.from_pretrained(base_name)
        model = AutoModel.from_pretrained(base_name).to(device)
        
        return SimilaritySearcher(
            model, tokenizer, max_length, device
        )
    
class InternetSearchStrategy(CtxStrategy):
    def __init__(
        self,
        similarity_searcher,
        instruction=default_instruction,
        serper_api_key=None, 
        db_name=None, chunk_size=1800
    ):
        self.searcher = similarity_searcher
        self.instruction = instruction
        self.db_name = db_name
        self.chunk_size = chunk_size
        self.serper_api_key=serper_api_key

        if self.searcher is None:
            raise ValueError("SimilaritySearcher is not set.")
        
        if self.serper_api_key is None:
            raise ValueError("API Key is not set. Grasp your own at https://serper.dev/")        
        
        if self.db_name is None:
            self.db_name = InternetSearchStrategy.id_generator()
        
    def __call__(self, ppmanager: PPManager, search_query=None, search_top_k=5, top_k=8, keep_original=False):
        ppm = copy.deepcopy(ppmanager)
        if search_query is None:
            search_query = ppm.pingpongs[-1].ping
        last_ping = ppm.pingpongs[-1].ping
        
        # 1st yield
        ppm.add_pong("![loading](https://i.ibb.co/RPSPL5F/loading.gif)\n")
        ppm.append_pong("• Creating Chroma DB Collection...")
        yield ppm, "• Creating Chroma DB Collection √"
        
        chroma_client = chromadb.Client()
        try:
            chroma_client.delete_collection(self.db_name)
        except:
            pass
        
        col = chroma_client.create_collection(self.db_name)
        
        # 2nd yield
        ppm.replace_last_pong("![loading](https://i.ibb.co/RPSPL5F/loading.gif)\n")
        ppm.append_pong("• Creating Chroma DB Collection √\n")
        ppm.append_pong("• Google searching...\n")
        yield ppm, "• Google searching √"

        urls = []
        titles = []
        search_results = []
        for search_result, title, url in self._google_search(search_query, search_top_k):
            search_results.append(search_result)
            titles.append(title)
            urls.append(url)
            
            ppm.append_pong(f"    - [{title}]({url}) √\n")
            yield ppm, f" ▷ [{title}]({url}) √"
        
        # 3rd yield
        ppm.replace_last_pong("![loading](https://i.ibb.co/RPSPL5F/loading.gif)\n")
        ppm.append_pong("• Creating Chroma DB Collection √\n")
        ppm.append_pong("• Google searching √\n")
        for title, url in zip(titles, urls):
            ppm.append_pong(f"    - [{title}]({url}) √\n")
        ppm.append_pong("• Creating embeddings...")
        yield ppm, "• Creating embeddings √"
        
        final_chunks = []
        for search_result in search_results:
            chunks = self._create_chunks(
                search_result, 
                chunk_size=self.searcher.max_length
            )
            final_chunks.append(chunks)  
            
        self._put_chunks_into_collection(
            col, final_chunks, docs_per_step=1
        )
        
        query_results = self._query(
            col, f"query: {last_ping}", top_k,
        )

        # 4th yield
        ppm.replace_last_pong("![loading](https://i.ibb.co/RPSPL5F/loading.gif)\n")
        ppm.append_pong("• Creating Chroma DB Collection √\n")
        ppm.append_pong("• Google searching √\n")
        for title, url in zip(titles, urls):
            ppm.append_pong(f"    - [{title}]({url}) √\n")
        ppm.append_pong("• Creating embeddings √\n")
        ppm.append_pong("• Information retrieval...")
        yield ppm, "• Information retrieval √"
        
        last_ping = self.instruction.format(ping=last_ping)
        for doc in query_results['documents'][0]:
            last_ping = last_ping + doc.replace('passage: ', '') + "\n"

        # 5th yield
        ppm.replace_last_pong("![loading](https://i.ibb.co/RPSPL5F/loading.gif)\n")
        ppm.append_pong("• Creating Chroma DB Collection √\n")
        ppm.append_pong("• Google searching √\n")
        for title, url in zip(titles, urls):
            ppm.append_pong(f"    - [{title}]({url}) √\n")
        ppm.append_pong("• Creating embeddings √\n")
        ppm.append_pong("• Information retrieval √")
        yield ppm, "• Done √"
            
        ppm.pingpongs[-1].ping = last_ping
        ppm.replace_last_pong("")
        yield ppm, "⏳ Wait until LLM generates message for you ⏳"
        
    def _google_search(self, query, search_top_k):
        search_results = self.__google_search(query, self.serper_api_key)

        final_results = []
        titles = []
        urls = []
        num_of_searched = 0

        for search_result in search_results:
            if num_of_searched >= search_top_k:
                break
            
            title = search_result['title']
            url = search_result['link']

            if url.startswith("https://youtube.com"):
                continue

            try: 
                page = urlopen(url, timeout=5)
                html_bytes = page.read()
                html = html_bytes.decode("utf-8")
            except:
                continue 
 
            ps = ""
            soup = BeautifulSoup(html, "html.parser")

            for tag in soup.findAll('p'):
                for string in tag.strings:
                    ps = ps + string

            ps = self._replace_multiple_newlines(ps)
            yield ps, title, url
            # final_results.append(ps)
            # urls.append(url)
            # titles.append(title)
            num_of_searched = num_of_searched+1

        # return final_results, titles, urls

    def __google_search(self, query, serper_key):
        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({
            "q": query
        })
        headers = {
            'X-API-KEY': serper_key,
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data)['organic']
    
    def _query(
        self, collection, q, top_k
    ):
        _, q_embeddings_list = self.searcher.get_embeddings([q])

        return collection.query(
            query_embeddings=q_embeddings_list,
            n_results=top_k
        )
    
    # chunk_size == number of characters
    def _create_chunks(self, text, chunk_size):
        chunks = []

        for idx in range(0, len(text), chunk_size):
            chunks.append(
                f"passage: {text[idx:idx+chunk_size]}"
            )

        return chunks
    
    def _put_chunk_into_collection(
        self, collection, chunk_id, chunk, docs_per_step=1
    ):
        for i in range(0, len(chunk), docs_per_step):
            cur_texts = chunk[i:i+docs_per_step]
            _, embeddings_list = self.searcher.get_embeddings(cur_texts)
            ids = [
                f"id-{chunk_id}-{num}" for num in range(i, i+docs_per_step)
            ]

            collection.add(
              embeddings=embeddings_list,
              documents=cur_texts,
              ids=ids
            )

    def _put_chunks_into_collection(
        self, collection,
        chunks, docs_per_step=1
    ):
        for idx, chunk in enumerate(chunks):
            self._put_chunk_into_collection(
                collection, idx, 
                chunk, docs_per_step=docs_per_step
            )

    def _replace_multiple_newlines(self, text):
        """Replaces multiple newline characters with a single newline character."""
        pattern = re.compile(r"\n+")
        return pattern.sub("\n", text)             
            
    @classmethod
    def id_generator(cls, size=10, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
