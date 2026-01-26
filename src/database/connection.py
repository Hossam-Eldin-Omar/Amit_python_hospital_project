"""ScyllaDB connection module for hospital project"""
import os
import socket
import time
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra import ConsistencyLevel

# Force IPv4 only (helps with Docker networking)
original_getaddrinfo = socket.getaddrinfo


def getaddrinfo_ipv4_only(host, port, family=0, type=0, proto=0, flags=0):
    return original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)


socket.getaddrinfo = getaddrinfo_ipv4_only


class ScyllaDBConnection:
    """Manages ScyllaDB connection for the hospital application"""

    def __init__(self):
        self.cluster = None
        self.session = None
        self.host = os.getenv("SCYLLA_HOST", "scylla-node")
        self.port = int(os.getenv("SCYLLA_PORT", "9042"))

    def connect(self, max_retries=5, retry_delay=5):
        """
        Establish connection to ScyllaDB.

        Args:
            max_retries: Number of connection attempts
            retry_delay: Seconds to wait between retries

        Returns:
            session: Cassandra session object
        """
        print(f"Connecting to ScyllaDB at {self.host}:{self.port}...")

        profile = ExecutionProfile(
            load_balancing_policy=DCAwareRoundRobinPolicy(local_dc="datacenter1"),
            request_timeout=30,
            consistency_level=ConsistencyLevel.ONE,
        )

        for attempt in range(max_retries):
            try:
                self.cluster = Cluster(
                    contact_points=[self.host],
                    port=self.port,
                    protocol_version=4,
                    execution_profiles={EXEC_PROFILE_DEFAULT: profile},
                    connect_timeout=15,
                )

                self.session = self.cluster.connect()

                # Verify connection
                row = self.session.execute(
                    "SELECT release_version FROM system.local"
                ).one()
                print(f"✓ Connected to ScyllaDB version: {row.release_version}")

                return self.session

            except Exception as e:
                print(f"Connection attempt {attempt + 1}/{max_retries} failed: {e}")

                if self.cluster:
                    try:
                        self.cluster.shutdown()
                    except:
                        pass

                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    raise Exception(
                        f"Failed to connect to ScyllaDB after {max_retries} attempts"
                    )

    def close(self):
        """Close the database connection"""
        if self.cluster:
            self.cluster.shutdown()
            print("✓ Database connection closed")

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Convenience function for backward compatibility
def get_scylla_connection(max_retries=5, retry_delay=5):
    """
    Create and return a ScyllaDB session.

    Returns:
        tuple: (cluster, session)
    """
    db = ScyllaDBConnection()
    session = db.connect(max_retries, retry_delay)
    return db.cluster, session


if __name__ == "__main__":
    # Test the connection
    print("=" * 60)
    print("Testing ScyllaDB Connection")
    print("=" * 60)

    try:
        with ScyllaDBConnection() as session:
            # Create a test keyspace
            session.execute(
                """
                CREATE KEYSPACE IF NOT EXISTS test_keyspace
                WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
            """
            )
            print("✓ Test keyspace created")

            print("✓ Connection test successful!")

    except Exception as e:
        print(f"✗ Connection test failed: {e}")
        import traceback

        traceback.print_exc()
        exit(1)
