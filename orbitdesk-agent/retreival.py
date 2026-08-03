from sentence_transformers import SentenceTransformer
from load import documents
import faiss
import numpy as np
import os 


model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = []

for docs in documents:
    result = model.encode(docs["content"])
    embeddings.append(result)
    # print(len(embeddings))
    
embeddings_np = np.array(embeddings)
dimension = embeddings_np.shape[1]
if os.path.exists("knowledge_base.index"):
    index = faiss.read_index("knowledge_base.index")
else:
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_np)
    faiss.write_index(index, "knowledge_base.index")
# print(index.ntotal)

def search(question , top_k = 3 ):
    query_embedding = model.encode(question).reshape(1,-1)
    distances, indices = index.search(query_embedding, top_k)
    results = []
    for i in indices[0]:
        results.append(documents[i])
    return results
    
    
