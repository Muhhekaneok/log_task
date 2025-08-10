import argparse
import json
from tabulate import tabulate


def process_files(file_paths):
    stats = {}

    for file_path in file_paths:
        try:
            with open(file_path, "r") as file:
                for line in file:
                    try:
                        log_data = json.loads(line)
                        url = log_data["url"]
                        time = log_data["response_time"]

                        if url not in stats:
                            stats[url] = {"count": 0, "total_time": 0.0}

                        stats[url]["count"] += 1
                        stats[url]["total_time"] += time

                    except json.JSONDecodeError:
                        continue

        except FileNotFoundError:
            print("File not found")
            continue

    report_data = []
    for url, data in stats.items():
        count = data["count"]
        total_time = data["total_time"]
        avg_time = total_time / count

        report_data.append([url, count, avg_time])

    return report_data


def main():
    parser = argparse.ArgumentParser(description="Analyzing log-files")
    parser.add_argument(
        "--file",
        nargs="+",
        required=True,
        help="Path to one or few log-files"
    )

    args = parser.parse_args()

    final_report = process_files(args.file)

    if not final_report:
        print("JSON lines not found")
        return

    # for row in final_report:
    #     url, count, avg_time = row
    #     print(f"Endpoint: {url}, Requests: {count}, Average time: {avg_time:.3f}")

    headers = ["Endpoint", "Request count", "Average time"]

    print(tabulate(final_report, headers=headers, tablefmt="grid", floatfmt=".3f"))

if __name__ == "__main__":
    main()
