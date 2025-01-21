import datetime
import random
from influxdb_client import InfluxDBClient, Point

# Define GNSS data structure
class GNSSData:
    def __init__(self, utc_time, latitude, longitude, speed, course, mode):
        self.utc_time = utc_time
        self.latitude = latitude
        self.longitude = longitude
        self.speed = speed
        self.course = course
        self.mode = mode

# Simulate GNSS data
def simulate_gnss_data():
    # Generate random values for latitude, longitude, speed, and course
    latitude = 47.28524 + (random.uniform(-0.001, 0.001)) * 100
    longitude = 8.56525 + (random.uniform(-0.001, 0.001)) * 100
    speed = random.uniform(0.0, 1.0)
    course = random.uniform(0.0, 360.0)

    # Create GNSS data object
    gnss_data = GNSSData(
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        latitude,
        longitude,
        speed,
        course,
        "A"
    )

    return gnss_data

# Write GNSS data to InfluxDB
def write_gnss_to_influx(gnss_data, write_api, bucket, org):
    # Create a point for InfluxDB
    point = (
        Point("location")
        .tag("device_id", "device123")
        .field("latitude", gnss_data.latitude)
        .field("longitude", gnss_data.longitude)
        .field("speed", gnss_data.speed)
        .field("course", gnss_data.course)
        .field("fix_status", 1)  # Assuming fix_status is always 1
        .field("mode", gnss_data.mode)
        .time(datetime.datetime.utcnow())
    )
    # Write the point to InfluxDB
    write_api.write(bucket=bucket, org=org, record=point)

# Main function
def main():
    # Read the InfluxDB token from the file
    with open('influx_token.txt', 'r') as f:
        token = f.read().strip()

    # InfluxDB configuration
    influx_url = "https://us-east-1-1.aws.cloud2.influxdata.com" 
    bucket = "canBus"  
    org = "formulaOne" 

    # Initialize the InfluxDB client
    client = InfluxDBClient(url=influx_url, token=token, org=org)
    write_api = client.write_api()

    try:
        # Simulate GNSS data
        gnss_data = simulate_gnss_data()

        # Write GNSS data to InfluxDB
        write_gnss_to_influx(gnss_data, write_api, bucket, org)

        print("GNSS data written to InfluxDB!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the client is closed properly
        write_api.__del__()  # Cleanly shutdown the write API
        client.close()


if __name__ == "__main__":
    main()
