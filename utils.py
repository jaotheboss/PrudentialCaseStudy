def mean(num_list: list) -> float:
    n = len(num_list)
    if n > 1:
        return sum(num_list) / n
    elif n == 1:
        return num_list[0]
    else:
        return 0

class ContextUtil:
    @staticmethod
    def validate_context(response, threshold = 0.75):
        """Validates whether a prompt was relevant to the source nodes"""
        relevance_score = mean([i.score for i in response.source_nodes])
        print(relevance_score)
        return relevance_score > threshold
    
# pip install rank-bm25 sentence_transformers
# from llama_index.retrievers import BaseRetriever
# from llama_index.postprocessor import SentenceTransformerRerank

# class HybridRetriever(BaseRetriever):
#     def __init__(self, vector_retriever, bm25_retriever):
#         self.vector_retriever = vector_retriever
#         self.bm25_retriever = bm25_retriever
#         super().__init__()

#     def _retrieve(self, query, **kwargs):
#         bm25_nodes = self.bm25_retriever.retrieve(query, **kwargs)
#         vector_nodes = self.vector_retriever.retrieve(query, **kwargs)

#         # combine the two lists of nodes
#         all_nodes = []
#         node_ids = set()
#         for n in bm25_nodes + vector_nodes:
#             if n.node.node_id not in node_ids:
#                 all_nodes.append(n)
#                 node_ids.add(n.node.node_id)
#         return all_nodes
    
# hybrid_retriever = HybridRetriever(1, 2)
# reranker = SentenceTransformerRerank(top_n=4, model="BAAI/bge-reranker-base")

