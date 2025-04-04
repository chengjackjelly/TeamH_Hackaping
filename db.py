import os
from datetime import timedelta
import traceback

# For exceptions
from couchbase.exceptions import CouchbaseException

# Required for any cluster connection
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster

# Required for options -- cluster, timeout, SQL++ (N1QL) query, etc.
from couchbase.options import ClusterOptions

endpoint = "couchbases://cb.ouhfvudxvxtyljm1.cloud.couchbase.com"  # Replace this with Connection String
username = "TEAMH"  # Replace this with username from cluster access credentials
password = os.getenv(
    "DB_PASSWORD"
)  # Replace this with password from cluster access credentials
bucket_name = "hackaping"
scope_name = "HardwareDestroyer"
collection_name = "Products"

auth = PasswordAuthenticator(username, password)
# Get a reference to our cluster
options = ClusterOptions(auth)
# Use the pre-configured profile below to avoid latency issues with your connection.
options.apply_profile("wan_development")
try:
    cluster = Cluster(endpoint, options)
    # Wait until the cluster is ready for use.
    cluster.wait_until_ready(timedelta(seconds=5))
    result = cluster.query("SELECT * from hackaping.HardwareDestroyer.RawMaterial")
    print(result)
    for row in result.rows():
        print(f"find row: {row}")
except Exception as e:
    traceback.print_exc()
