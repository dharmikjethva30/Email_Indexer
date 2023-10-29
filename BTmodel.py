from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import random

# Initialize Elasticsearch client
es = Elasticsearch("https://localhost:9200/", ca_certs="E:\Elastic-stack\elasticsearch-8.10.4\config\certs\http_ca.crt", basic_auth=("elastic", "LVZoeD*lowJfc=JiD7x4"))

# Initialize the language models
bigram_model = {}
trigram_model = {}

# Function to generate n-grams
def generate_ngrams(tokens, n):
    n_grams = ngrams(tokens, n)
    return list(n_grams)

# Tokenize and generate n-grams from email text
def process_email(email_text):
    tokens = word_tokenize(email_text)
    bigrams = generate_ngrams(tokens, 2)
    trigrams = generate_ngrams(tokens, 3)
    return tokens, bigrams, trigrams

# Retrieve email text from Elasticsearch and build the models
query = {
    "query": {
        "match": {
            'from':'Director'
        }
    }
}

# Use the scroll API to retrieve all emails
emails = scan(es, index="email_index123", query=query)

for email in emails:
    email_text = email["_source"]["body"]
    tokens, bigrams, trigrams = process_email(email_text)
    
    # Update the language models with bigrams and trigrams
    for bigram in bigrams:
        prefix, suffix = bigram
        if prefix not in bigram_model:
            bigram_model[prefix] = []
        bigram_model[prefix].append(suffix)
    
    for trigram in trigrams:
        prefix, suffix = trigram[:2], trigram[2]
        if prefix not in trigram_model:
            trigram_model[prefix] = []
        trigram_model[prefix].append(suffix)

# Function to generate text using bigram model
def generate_bigram_text(bigram_model, seed_word, max_length=20):
    text = [seed_word]
    current_word = seed_word
    for _ in range(max_length - 1):
        if current_word not in bigram_model:
            break
        next_word = random.choice(bigram_model[current_word])
        text.append(next_word)
        current_word = next_word
    return " ".join(text)

# Function to generate text using trigram model

def generate_trigram_text(trigram_model, seed_prefix, max_length=20):
    text = list(seed_prefix)
    current_prefix = tuple(seed_prefix)  # Convert the prefix to a tuple
    for _ in range(max_length - len(seed_prefix)):
        if current_prefix not in trigram_model:
            break
        next_word = random.choice(trigram_model[current_prefix])
        text.append(next_word)
        current_prefix = tuple(text[-2:])  # Update current_prefix as a tuple
    return " ".join(text)


# Generate random text for a seed word
seed_word = "Students"  # Change to your desired seed word
max_length = 10  # Adjust the maximum length of the generated text

# Generate bigram text for the seed word
generated_bigram_text = generate_bigram_text(bigram_model, seed_word, max_length)
print("Generated Bigram Text:")
print(generated_bigram_text)

# Generate random text for a seed prefix
seed_prefix = ("Dear","Sir")  # Change to your desired seed prefix
max_length = 50  # Adjust the maximum length of the generated text

# Generate trigram text for the seed prefix
generated_trigram_text = generate_trigram_text(trigram_model, seed_prefix, max_length)
print("\nGenerated Trigram Text:")
print(generated_trigram_text)
