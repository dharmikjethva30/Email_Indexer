from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch("https://localhost:9200/", ca_certs="E:\Elastic-stack\elasticsearch-8.10.4\config\certs\http_ca.crt", basic_auth=("elastic", "LVZoeD*lowJfc=JiD7x4"))

# Define your date range query
search_query = {
    "query": {
        "match": {
            "body": "information"  # Change to your desired keywords
        }
    }
}

# Execute the query
result = es.search(index="email_index123", body=search_query)

# Process and print the search results
for hit in result["hits"]["hits"]:
    print(f"Subject: {hit['_source']['subject']}")
