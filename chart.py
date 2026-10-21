
import json
import matplotlib.pyplot as plt


def create_temperature_chart(json_file):
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"Error loading JSON: {error}")
        return

    if not data:
        print("No data available to plot.")
        return

    devices = [item["device_id"] for item in data]
    temperatures = [
        item["average_temperature"] for item in data
    ]

    plt.figure(figsize=(9, 5))
    bars = plt.bar(devices, temperatures)

    plt.title("Average Temperature per Device")
    plt.xlabel("Device ID")
    plt.ylabel("Average Temperature (°C)")
    plt.xticks(rotation=0)
    plt.ylim(0, max(temperatures) * 1.15)

    for bar, temperature in zip(bars, temperatures):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{temperature:.2f}",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()
    plt.savefig("temperature_chart.png", dpi=150)
    print("Chart saved as temperature_chart.png")
    plt.show()


if __name__ == "__main__":
    create_temperature_chart("summary.json")
