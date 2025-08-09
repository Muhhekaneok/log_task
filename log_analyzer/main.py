import json

stats = {}

file_name = "example1.log"

with open(file_name, "r") as file:
    for line in file:
        log_data = json.loads(line)

        url = log_data["url"]
        time = log_data["response_time"]

        if url not in stats:
            stats[url] = {"count": 0, "total_time": 0.0}

        stats[url]["count"] += 1
        stats[url]["total_time"] += time

for url, data in stats.items():
    count = data["count"]
    total_time = data["total_time"]

    avg_time = total_time / count

    print(f"Endpoint: {url}")
    print(f"\tRequest count: {count}")
    print(f"\tAverage time response: {avg_time:.3f}")
    print("-" * 20)