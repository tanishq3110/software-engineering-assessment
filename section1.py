
def clean_sensor_readings(readings):
    cleaned = []

    for value in readings:
        if value is None:
            continue
        try:
            number = float(value)
        except (ValueError, TypeError):
            continue
        if number < 0:
            continue
        if number > 500.0:
            number = 500.0
        cleaned.append(number)
    return cleaned


readings1 = [10, "25.5", None, -5, 700, "abc"]
print(clean_sensor_readings(readings1))

readings2 = [None, -1, "hello"]
print(clean_sensor_readings(readings2))

readings3 = []
print(clean_sensor_readings(readings3))

