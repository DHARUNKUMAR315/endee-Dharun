import csv
import endee
import time
from sentence_transformers import SentenceTransformer

def run_pipeline():
    print("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("Connecting to Endee Vector Database...")
    client = endee.Endee()
    index_name = "enterprise_tickets_index"
    
    indexes_resp = client.list_indexes()
    index_names = [i['name'] for i in indexes_resp.get('indexes', [])]
    
    if index_name in index_names:
        print(f"Index {index_name} already exists. Deleting strictly to ensure clean pipeline data...")
        client.delete_index(index_name)
        time.sleep(2)
        
    print(f"Creating highly scaled new index: {index_name} (dim=384)")
    client.create_index(name=index_name, dimension=384, space_type="cosine")
    index = client.get_index(index_name)
    
    print("Reading and embedding 1,000 synthetic tickets from tickets.csv...")
    tickets = []
    with open('tickets.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tickets.append(row)
            
    # Batch process upserts safely
    BATCH_SIZE = 100
    for i in range(0, len(tickets), BATCH_SIZE):
        batch_slice = tickets[i:i + BATCH_SIZE]
        texts = [t['description'] for t in batch_slice]
        
        print(f"Encoding vector batch {i} to {i + len(batch_slice)}")
        embeddings = model.encode(texts).tolist()
        
        upsert_payload = []
        for j, t in enumerate(batch_slice):
            upsert_payload.append({
                "id": t['id'],
                "vector": embeddings[j],
                "meta": {
                    "title": t['title'],
                    "text": t['description'],
                    "category": t['category'],
                    "resolution": t['resolution'],
                    "priority": t['priority']
                }
            })
            
        print("Upserting payload into Endee...")
        index.upsert(upsert_payload)

    print("Data Pipeline Completed. 1,000 unified tickets fully indexed!")

if __name__ == "__main__":
    run_pipeline()
