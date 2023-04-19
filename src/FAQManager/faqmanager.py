from sentence_transformers import SentenceTransformer, util
from helpdesk_app.models import Category, Query
import torch

embedder = SentenceTransformer('all-MiniLM-L6-v2')

class FAQManager:

    def get_top_queries(limit=5, category=None):
        top_queries = None
        if category:
            top_queries = Query.objects.filter(category=category).order_by('-occurrences')[:limit]
        else:
            top_queries = Query.objects.order_by('-occurrences')[:limit]
        
        return top_queries

    def recalculate():
        categories = list(Category.objects.all())
        
        # Append None to account for queries without a category
        categories.append(None)

        for category in categories:
            old_queries = Query.objects.filter(category=category).exclude(encoded_query=None)
            old_query_encodings = list(map(lambda query: query.encoded_query, old_queries))

            new_queries = Query.objects.filter(category=category).filter(encoded_query=None)
            if len(new_queries) == 0:
                continue

            new_processed_queries = list(map(lambda query: query.processed_query, new_queries))
            new_query_encodings = list(embedder.encode(new_processed_queries, convert_to_tensor=True, show_progress_bar=False))

            # Save the encodings for new queries
            for query, encoding in zip(new_queries, new_query_encodings):
                query.encoded_query = encoding
                query.save()

            if len(new_queries) > 1:
                encodings = torch.stack(old_query_encodings + new_query_encodings)
                clusters = util.community_detection(encodings, min_community_size=1, threshold=0.65)

                for i, cluster in enumerate(clusters):
                    total_occurrences = 0
                    for query_idx in cluster:
                        if query_idx >= len(old_queries):
                            total_occurrences += new_queries[query_idx - len(old_queries)].occurrences
                        else:
                            total_occurrences += old_queries[query_idx].occurrences
                    
                    # Arbitrarily pick one query to represent the cluster
                    cluster_leader = None
                    if cluster[0] >= len(old_queries):
                        cluster_leader = new_queries[cluster[0] - len(old_queries)]
                    else:
                        cluster_leader = old_queries[cluster[0]]
                    
                    cluster_leader.occurrences = total_occurrences
                    cluster_leader.save()

                    # Delete the remaining queries in the same cluster
                    for query_idx in cluster[1:]:
                        if query_idx >= len(old_queries):
                            new_queries[query_idx - len(old_queries)].delete()
                        else:
                            old_queries[query_idx].delete()