import json
from faker import Faker
from faker_vehicle import VehicleProvider

def generate_data(num_docs):
    fake = Faker()
    fake.add_provider(VehicleProvider)
    with open('vehicles.json', 'w') as outfile:
        for i in range(num_docs):
            doc = {
                'make': fake.vehicle_make(),
                'model': fake.vehicle_model(),
                'count': fake.pyint(min_value=1, max_value=100),
                'timestamp': fake.date_time_between(start_date='-1y').isoformat()
            }
            json.dump(doc, outfile)
            outfile.write('\n')
            

if __name__ == '__main__':
    print("Generating data...")
    generate_data(10000000)