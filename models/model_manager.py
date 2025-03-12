from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline, HuggingFaceEmbeddings
import torch
from config import MODEL_ID, EMBEDDING_MODEL_NAME, MAX_LENGTH, REPETITION_PENALTY
from utils.logger import get_logger

logger = get_logger(__name__)

class ModelManager:
    def __init__(self):
        self.llm = None
        self.embedding_model = None

    def initialize_models(self):
        try:
            tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
            model = AutoModelForCausalLM.from_pretrained(
                MODEL_ID,
                device_map="auto",
                torch_dtype=torch.float32
            )
            # Check if CUDA is available
            device = 0 if torch.cuda.is_available() else -1
            print(f"Using device: {'GPU' if device == 0 else 'CPU'}")
            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_length=MAX_LENGTH,
                repetition_penalty=REPETITION_PENALTY,
                pad_token_id=tokenizer.eos_token_id,
                truncation=True  
            )
            self.llm = HuggingFacePipeline(pipeline=pipe)
            self.embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
            logger.info("Models initialized successfully.")
            return True
        except Exception as e:
            logger.error(f"Error initializing models: {str(e)}")
            return False
