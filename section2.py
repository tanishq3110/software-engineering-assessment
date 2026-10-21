
import csv
import json
from collections import defaultdict


def process_telemetry(csv_file, json_file):
    devices = defaultdict(lambda: {
        "total_records": 0,
        "temperature_sum": 0.0,
        "error_count": 0
    })

    try:
        with open(csv_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            required = {"device_id", "status", "temperature"}
            if not required.issubset(reader.fieldnames or []):
                raise ValueError("CSV is missing required columns.")

            for row in reader:
                try:
                    device_id = row["device_id"].strip()
                    status = row["status"].strip().upper()
                    temperature = float(row["temperature"])

                    if not device_id:
                        continue

                except (ValueError, TypeError, AttributeError):
                    continue

                device = devices[device_id]
                device["total_records"] += 1
                device["temperature_sum"] += temperature

                if status == "ERROR":
                    device["error_count"] += 1

    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return

    results = []

    for device_id, data in devices.items():
        average = data["temperature_sum"] / data["total_records"]

        if average <= 80.0:
            results.append({
                "device_id": device_id,
                "total_records": data["total_records"],
                "average_temperature": round(average, 2),
                "error_count": data["error_count"]
            })

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)

    print(f"{'Device':<12}{'Records':<12}"
          f"{'Avg Temp':<12}{'Errors':<10}")
    print("-" * 46)

    for item in results:
        print(
            f"{item['device_id']:<12}"
            f"{item['total_records']:<12}"
            f"{item['average_temperature']:<12}"
            f"{item['error_count']:<10}"
        )

    print(f"\nResults saved to {json_file}")


if __name__ == "__main__":
    process_telemetry("device_telemetry.csv", "summary.json")
