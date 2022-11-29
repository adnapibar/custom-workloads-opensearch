Benchmark with custom workload with fake data
===

The repository contains some helper scripts to setup an EC2 machine and bulk index generate data.

### Modify existing workload with additional operation 

**Copy and modify the nyc-taxis workload**

```
mkdir ~/workloads
cd workloads
cp -r .benchmark/benchmarks/default/nyc_taxis .
```

modify `operations/default.json` directory to add the new operation e.g.

```
{
    "name": "date_histogram_subaggs",
    "operation-type": "search",
    "body": {
        "size": 0,
        "query": {
            "range": {
                "dropoff_datetime": {
                    "gte": "2015-01-01 00:00:00",
                    "lte": "2015-01-01 23:59:59"
                }
            }
        },
        "aggs": {
            "dropoffs_over_time": {
                "date_histogram": {
                    "field": "dropoff_datetime",
                    "interval": "60s"
                },
                "aggs": {
                    "payment_type": {
                        "terms": {
                            "field": "payment_type"
                        },
                        "aggs": {
                            "total_payment_amount": {
                                "sum": {
                                    "field": "total_amount"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
```

Include the operation in the `append-no-conflicts` section in `test_procedures/default.json`

**Downlaod OpenSearch 2.4 & run benchmark tests**

Download a version of OpenSearch and start the instance

```
wget https://artifacts.opensearch.org/releases/core/opensearch/2.4.0/opensearch-min-2.4.0-linux-x64.tar.gz
tar -xf opensearch-min-2.4.0-linux-x64.tar.gz
cd opensearch-2.4.0
nohup ./bin/opensearch &>>os.log &
```

Run the benchmark 

```
opensearch-benchmark execute_test --pipeline=benchmark-only --target-hosts=127.0.0.1:9200 --distribution-version=2.4.0 --workload-path=/home/ubuntu/workloads/nyc_taxis --test-procedure=append-no-conflicts
```

### Generate fake data & run workload

The `bulk_ingest.py` script generates 10,000,000 documents of fake vehicle sales data and bulk indexes into the cluster.

Install `Faker` and `opensearchpy` for this.

The workloads directory contains a workload for vehicles data, run the workload by running

```
opensearch-benchmark execute_test --pipeline=benchmark-only --target-hosts=127.0.0.1:9200 --distribution-version=2.4.0 --workload-path=/home/ubuntu/workloads/vehicles
```

