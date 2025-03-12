MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# parameters for text generation pipeline
MAX_LENGTH = 2048
REPETITION_PENALTY = 1.15

# parameter for spliting text into chunks
CHUNK_SIZE = 512
CHUNK_OVERLAP = 64

# parameters for search in vector database
SEARCH_K = 5
