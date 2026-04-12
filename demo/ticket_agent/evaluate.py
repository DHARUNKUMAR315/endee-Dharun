import csv
import endee
import time
from sentence_transformers import SentenceTransformer
from sklearn.metrics import accuracy_score, f1_score

def run_evaluation():
    print("Loading AI Model and Endee Client for Evaluation...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    client = endee.Endee()
    
    try:
        index = client.get_index("enterprise_tickets_index")
    except Exception as e:
        print(f"Error accessing index: {e}")
        return

    print("Loading evaluation split (taking 100 random samples from dataset)...")
    import random
    tickets = []
    with open('tickets.csv', 'r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
        
    random.seed(42)
    test_split = random.sample(reader, 100)
    
    y_true = []
    y_pred = []
    
    print("\nStarting inference evaluation pipeline...\n")
    start_time = time.time()
    
    for i, t in enumerate(test_split):
        query = t['description']
        true_category = t['category']
        
        vector = model.encode(query).tolist()
        results = index.query(vector=vector, top_k=1)
        
        if results and len(results) > 0:
            pred_category = results[0]['meta']['category']
        else:
            pred_category = "ESCALATED"
            
        y_true.append(true_category)
        y_pred.append(pred_category)
        
    total_time = time.time() - start_time
    avg_latency = (total_time / 100) * 1000
    
    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average='weighted')
    
    print("="*40)
    print("🚀 AUTOMATED AGENT EVALUATION METRICS")
    print("="*40)
    print(f"Total Test Samples   : 100")
    print(f"Average AI Latency   : {avg_latency:.2f} ms")
    print(f"Global Routing Acc   : {acc*100:.1f}%")
    print(f"Weighted F1 Score    : {f1*100:.1f}%")
    print("="*40)
    print("Evaluation Complete. Project fully mapped.")

if __name__ == "__main__":
    run_evaluation()
