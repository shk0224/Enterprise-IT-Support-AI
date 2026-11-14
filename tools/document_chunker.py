# ==========================================
# SECTION 1: IMPORTS
# ==========================================
from typing import Iterable
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==========================================
# SECTION 2: CHUNK DOCUMENTS
# ==========================================
def chunk_documents(docs: Iterable[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=120, add_start_index=True)
    return splitter.split_documents(list(docs))
