from faker import Faker
from faker_vehicle import VehicleProvider
import json
from opensearchpy import OpenSearch
from opensearchpy.helpers import streaming_bulk
from opensearchpy import OpenSearch
from opensearchpy.helpers import streaming_bulk
import tqdm


def create_index(client):
    """Creates an index in Elasticsearch if one isn't already there."""
    client.indices.create(
        index="vehicles",
        body={
            "settings": {"number_of_shards": 1},
            "mappings": {
                "properties": {
                    "make": {"type": "keyword"},
                    "model": {"type": "keyword"},
                    "count": {"type": "integer"},
                    "timestamp": {"type": "date"}
                }
            },
        },
        ignore=400,
    )


def generate_data(num_docs):
    fake = Faker()
    fake.add_provider(VehicleProvider)
    for i in range(num_docs):
        doc = {
            'make': fake.vehicle_make(),
            'model': fake.vehicle_model(),
            'count': fake.pyint(min_value=1, max_value=100),
            'timestamp': fake.date_time_this_month().isoformat()
        }
        yield doc


if __name__ == '__main__':
    number_of_docs = 10000000
    client = OpenSearch()
    print("Creating an index...")
    create_index(client)

    print("Indexing documents...")
    progress = tqdm.tqdm(unit="docs", total=number_of_docs)
    successes = 0
    for ok, action in streaming_bulk(
        client=client, index="vehicles", actions=generate_data(number_of_docs),
    ):
        progress.update(1)
        successes += ok
    print("Indexed %d/%d documents" % (successes, number_of_docs))
