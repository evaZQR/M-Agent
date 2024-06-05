import os
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from transformers import BitsAndBytesConfig, AutoModelForCausalLM, AutoTokenizer
from typing import Optional, List, Mapping, Any
import torch
from llama_index.core.llms.callbacks import llm_chat_callback, llm_completion_callback
from llama_index.core.llms import (
    CustomLLM,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
)


class OurModel(CustomLLM):
    context_window: int = 4096
    num_output: int = 1024
    model_name: str = "custom"

    def __init__(self, model: Any, tokenizer: Any):
        self.model = model
        self.tokenizer = tokenizer

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            model_name=self.model_name,
            num_output=self.num_output,
            context_window=self.context_window,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        text, history = self.model.chat(self.tokenizer, prompt, history=[], temperature=0.1)
        return CompletionResponse(text=text)

    @llm_chat_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        def gen() -> CompletionResponseGen:
            text = ""
            for ch in prompt:  # Simulate streaming response
                text += ch
                yield CompletionResponse(
                    text=text,
                    delta=ch,
                    additional_kwargs={"prompt": prompt},
                )
        return gen()

def get_llm(model_path: str) -> OurModel:
    model_path = "./checkpoint/chatglm3-6b"
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, trust_remote_code=True, low_cpu_mem_usage = True ,quantization_config=quantization_config).eval()
    return OurModel(model, tokenizer)

def get_embed_model(model_path: str) -> HuggingFaceEmbedding:
    return HuggingFaceEmbedding(model_name = model_path)

