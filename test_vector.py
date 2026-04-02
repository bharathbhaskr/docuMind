from services.vector_service import store_chunks, search_chunks, delete_collection

# Clean up any previous test runs
delete_collection("test_collection")

# Some sample text chunks - imagine these came from a PDF
sample_chunks = [
    "Paris is the capital city of France and its largest city.",
    "The Eiffel Tower was built in 1889 and stands 330 meters tall.",
    "France is a country in Western Europe with a population of 68 million.",
    "Python is a programming language known for its simplicity.",
    "Machine learning models require large amounts of training data.",
    "The Seine river flows through the heart of Paris.",
]

print("Storing chunks...")
count = store_chunks("test_collection", sample_chunks)
print(f"Stored {count} chunks\n")

# Test 1 - should find Paris/France chunks, NOT Python chunks
print("--- Search 1: 'What is the capital of France?' ---")
results = search_chunks("test_collection", "What is the capital of France?", n_results=2)
for i, chunk in enumerate(results):
    print(f"  Result {i+1}: {chunk}")

print()

# Test 2 - should find Eiffel Tower chunk
print("--- Search 2: 'How tall is the famous tower in Paris?' ---")
results = search_chunks("test_collection", "How tall is the famous tower in Paris?", n_results=2)
for i, chunk in enumerate(results):
    print(f"  Result {i+1}: {chunk}")

print()

# Test 3 - semantic match with different words
print("--- Search 3: 'Tell me about AI and data' ---")
results = search_chunks("test_collection", "Tell me about AI and data", n_results=2)
for i, chunk in enumerate(results):
    print(f"  Result {i+1}: {chunk}")