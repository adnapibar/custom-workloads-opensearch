import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk


def create_index(client):
    """Creates an index in Elasticsearch if one isn't already there."""
    client.indices.create(
        index="vehicles",
        body={
            "settings": {"number_of_shards": 1},
            "mappings": {
                "_doc": {
                    "properties": {
                        "make": {"type": "keyword"},
                        "model": {"type": "keyword"},
                        "count": {"type": "integer"},
                        "timestamp": {"type": "date"}
                    }
                }
            },
        },
        ignore=400,
    )


def generate_data():
    with open('vehicles.json', 'r') as file:
        for doc in file:
            yield doc


if __name__ == '__main__':
    number_of_docs = 10000000
    client = Elasticsearch()
    print("Creating an index...")
    create_index(client)

    print("Indexing documents...")
    progress = tqdm.tqdm(unit="docs", total=number_of_docs)
    successes = 0
    for ok, action in streaming_bulk(
        client=client, index="vehicles", doc_type="_doc", actions=generate_data(),
    ):
        progress.update(1)
        successes += ok
    print("Indexed %d/%d documents" % (successes, number_of_docs))
