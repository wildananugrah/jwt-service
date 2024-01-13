from datetime import datetime
import requests
import json
import threading
import time

host = "http://localhost:5000"
separator = ";"

# Duration for which to run the simulation (10 minutes)
duration = 1 * 60  # 10 minutes in seconds

print(f"{'time'}{separator}{'userid'}{separator}{'status_code'}{separator}{'content'}{separator}{'response_time'}")

def task(id):
    response = requests.post(f"{host}/token", json={ "username" : "wildananugrah", "age" : 32 })
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{separator}{id}{separator}{response.status_code}{separator}{response.content}{separator}{response.elapsed.total_seconds()}")

    token = response.json()['token']
    response = requests.post(f"{host}/validate", json={ "token": token })
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{separator}{id}{separator}{response.status_code}{separator}{response.content}{separator}{response.elapsed.total_seconds()}")

    response = requests.post(f"{host}/refresh", json={ "token": token })
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{separator}{id}{separator}{response.status_code}{separator}{response.content}{separator}{response.elapsed.total_seconds()}")


# task(1)

def simulate_user(id):
    while time.time() < end_time:
        task(id)

# Calculate end time
end_time = time.time() + duration

threads = []

for i in range(1, 21):
    thread = threading.Thread(target=simulate_user, args=(i,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("All user simulations completed.")

