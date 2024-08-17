from typing import Dict
from transformers import AutoTokenizer
from .configModels import AvailableTokenizers

class TokenizerManager:
    def __init__(self, available_tokenizers: AvailableTokenizers):
        """Manages the tokenizer available for the application."""
        self.tokenizers: Dict[str, AutoTokenizer] = {
            tokenizer: AutoTokenizer.from_pretrained(tokenizer) for tokenizer in available_tokenizers.AVAILABLE_TOKENIZERS
        }

    def get_tokenizer(self, name: str) -> AutoTokenizer:
        if name not in self.tokenizers:
            raise ValueError(f"Invalid tokenizer specified: {name}")
        return self.tokenizers[name]
