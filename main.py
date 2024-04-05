from collections import defaultdict
from datetime import datetime
import requests
import json
import configparser
import matplotlib.pyplot as plt


def get_credentials():
    config = configparser.ConfigParser()
    config.read("config.ini")  # Make sure config.ini is in the same directory

    email = config.get("OTF", "email")
    password = config.get("OTF", "password")

    if not email or not password:
        raise ValueError("OTF credentials not found in config.ini.")

    return email, password


# Simplified token retrieval
def get_token(email, password):
    header = '{"Content-Type": "application/x-amz-json-1.1", "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth"}'
    body = f'{{"AuthParameters": {{"USERNAME": "{email}", "PASSWORD": "{password}"}}, "AuthFlow": "USER_PASSWORD_AUTH", "ClientId": "65knvqta6p37efc2l3eh26pl5o"}}'
    response = requests.post(
        "https://cognito-idp.us-east-1.amazonaws.com/",
        headers=json.loads(header),
        json=json.loads(body),
    )
    return json.loads(response.content)["AuthenticationResult"]["IdToken"]


# Retrieve the list of workouts
def get_in_studio_response(token):
    endpoint = "https://api.orangetheory.co/virtual-class/in-studio-workouts"
    header = {"Content-Type": "application/json", "Authorization": token}
    return requests.get(endpoint, headers=header).json()


# Retrieve detailed workout data
def get_detailed_workout_data(class_history_uuid, member_uuid, token):
    endpoint = "https://performance.orangetheory.co/v2.4/member/workout/summary"
    headers = {"Content-Type": "application/json", "Authorization": token}
    payload = {"ClassHistoryUUId": class_history_uuid, "MemberUUId": member_uuid}
    response = requests.post(endpoint, headers=headers, json=payload)
    return response.json()


# Format Date to YYYY_MM_DD
def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date_obj.strftime("%Y-%m-%d")


def get_workout_summary(workouts_data, token):
    hr_totals = {}
    min_count = {}
    secs_in_zone = {"Red": 0, "Orange": 0, "Green": 0, "Blue": 0, "Black": 0}
    data_class_counter = 0
    max_hr_average_total = 0
    average_hr_total = 0
    average_splats_total = 0
    average_calories_total = 0
    for workout in workouts_data:
        data_class_counter += 1
        count = 1
        if "minuteByMinuteHr" in workout and workout["minuteByMinuteHr"] is not None:
            for hr in (
                workout["minuteByMinuteHr"].split("[")[1].split("]")[0].split(",")
            ):
                if count in hr_totals:
                    hr_totals[count] = int(hr_totals[count]) + int(hr)
                else:
                    hr_totals[count] = int(hr)
                if count in min_count:
                    min_count[count] = min_count[count] + 1
                else:
                    min_count[count] = 1
                count += 1
        secs_in_zone["Red"] += workout["redZoneTimeSecond"]
        secs_in_zone["Orange"] += workout["orangeZoneTimeSecond"]
        secs_in_zone["Green"] += workout["greenZoneTimeSecond"]
        secs_in_zone["Blue"] += workout["blueZoneTimeSecond"]
        secs_in_zone["Black"] += workout["blackZoneTimeSecond"]
        max_hr_average_total += workout["maxHr"]
        average_hr_total += workout["avgHr"]
        average_splats_total += workout["totalSplatPoints"]
        average_calories_total += workout["totalCalories"]
    return {
        "hr_totals": hr_totals,
        "min_count": min_count,
        "secs_in_zone": secs_in_zone,
        "data_class_counter": data_class_counter,
        "max_hr_average_total": max_hr_average_total,
        "average_hr_total": average_hr_total,
        "average_splats_total": average_splats_total,
        "average_calories_total": average_calories_total,
    }


def process_workouts(data, token, start_date=None, end_date=None):
    class_type_counter = defaultdict(int)
    classes_by_coach_and_studio = defaultdict(int)
    classes_by_location = defaultdict(int)
    workouts_filtered = []
    total_workouts = 0
    total_distance = 0.0
    max_speed = 0.0
    total_calories = 0
    total_splat_points = 0
    personal_bests = {
        "Max Speed": {"value": 0, "date": ""},
        "Max Distance": {"value": 0, "date": ""},
        "Max Calories": {"value": 0, "date": ""},
        "Max Splat Points": {"value": 0, "date": ""},
    }

    for workout in data:
        class_date_str = workout["classDate"]
        class_date = datetime.strptime(class_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")

        if (start_date is None or class_date >= start_date) and (
            end_date is None or class_date <= end_date
        ):
            workouts_filtered.append(workout)
            total_workouts += 1
            class_type_counter[workout.get("classType", "No Class Type Found")] += 1
            coach = workout.get("coach", "No Coach")
            studio_name = workout.get("studioName", "No Studio")
            classes_by_coach_and_studio[f"{coach} - {studio_name}"] += 1
            classes_by_location[studio_name] += 1
            class_history_uuid = workout["classHistoryUuId"]
            member_uuid = workout["memberUuId"]
            detailed_data = get_detailed_workout_data(
                class_history_uuid, member_uuid, token
            )
            treadmill_data = detailed_data.get("TreadmillData", {})
            heart_rate_data = detailed_data.get("HeartRateData", {})
            distance = treadmill_data.get("TotalDistance", {}).get("Value", 0.0)
            current_max_speed = treadmill_data.get("MaxSpeed", {}).get("Value", 0.0)
            calories = heart_rate_data.get("Calories", 0)
            splat_points = heart_rate_data.get("SplatPoint", 0)
            total_distance += distance
            max_speed = max(max_speed, current_max_speed)
            total_calories += calories
            total_splat_points += splat_points

            formatted_date = class_date.strftime("%Y-%m-%d")

            if distance > personal_bests["Max Distance"]["value"]:
                personal_bests["Max Distance"]["value"] = distance
                personal_bests["Max Distance"]["date"] = formatted_date
            if current_max_speed > personal_bests["Max Speed"]["value"]:
                personal_bests["Max Speed"]["value"] = current_max_speed
                personal_bests["Max Speed"]["date"] = formatted_date
            if calories > personal_bests["Max Calories"]["value"]:
                personal_bests["Max Calories"]["value"] = calories
                personal_bests["Max Calories"]["date"] = formatted_date
            if splat_points > personal_bests["Max Splat Points"]["value"]:
                personal_bests["Max Splat Points"]["value"] = splat_points
                personal_bests["Max Splat Points"]["date"] = formatted_date

    current_date = datetime.now()
    days_elapsed = (current_date - start_date).days + 1 if start_date else None
    workout_percentage = (total_workouts / days_elapsed) * 100 if days_elapsed else None
    workout_summary = get_workout_summary(workouts_filtered, token)

    return (
        class_type_counter,
        classes_by_coach_and_studio,
        classes_by_location,
        workouts_filtered,
        total_distance,
        max_speed,
        total_calories,
        total_splat_points,
        personal_bests,
        total_workouts,
        days_elapsed,
        workout_percentage,
        workout_summary["hr_totals"],
        workout_summary["min_count"],
        workout_summary["secs_in_zone"],
        workout_summary["data_class_counter"],
        workout_summary["max_hr_average_total"],
        workout_summary["average_hr_total"],
        workout_summary["average_splats_total"],
        workout_summary["average_calories_total"],
    )


def print_workout_stats(
    class_type_counter,
    classes_by_coach_and_studio,
    classes_by_location,
    workouts_filtered,
    total_distance,
    max_speed,
    total_calories,
    total_splat_points,
    personal_bests,
    total_workouts,
    days_elapsed,
    workout_percentage,
    hr_totals,
    min_count,
    secs_in_zone,
    data_class_counter,
    max_hr_average_total,
    average_hr_total,
    average_splats_total,
    average_calories_total,
):
    print("----------------------\n")
    print("Workouts in the selected date range:")
    print(f"Total workouts: {total_workouts}")

    if days_elapsed:
        print(f"Total number of days in the selected date range: {days_elapsed}")
        print(f"Percentage of workouts attended: {workout_percentage:.2f}")
    else:
        print(
            "Total number of days and workout percentage not available for the selected date range."
        )

    print("----------------------\n")
    print("Classes by type in the selected date range:")
    for class_type, count in class_type_counter.items():
        print(f"{class_type}: {count}")
    print("----------------------\n")
    print("Classes by coach and studio in the selected date range:")
    for coach_studio, count in classes_by_coach_and_studio.items():
        print(f"{coach_studio}: {count}")
    print("----------------------\n")
    print("Classes by location in the selected date range:")
    for location, count in classes_by_location.items():
        print(f"{location}: {count}")
    print("----------------------\n")
    print(f"Totals for the selected date range:")
    print(f"Total Distance: {total_distance:.2f} miles")
    print(f"Total Calories Burned: {total_calories:,.0f}")
    print(f"Total Splat Points: {total_splat_points}")
    print("----------------------\n")
    print("Personal Bests:")
    for metric, record in personal_bests.items():
        value = record["value"]
        date = record["date"]
        print(f"{metric}: {value} (on {date})")
    print("----------------------\n")
    print(
        f"The remainder of the data is based on workout summaries available for the selected date range. You have {data_class_counter} workouts with data available."
    )
    if data_class_counter > 0:
        print(f"Average Max HR: {max_hr_average_total / data_class_counter:.0f}")
        print(f"Average HR: {average_hr_total / data_class_counter:.0f}")
        print(f"Average Splats: {average_splats_total / data_class_counter:.0f}")
        print(
            f"Average calorie burn: {average_calories_total / data_class_counter:.0f}"
        )
        print("----------------------\n")
        print("Average HR by Min:")
        for minute in range(1, max(hr_totals.keys()) + 1):
            if minute in hr_totals:
                average_hr = hr_totals[minute] / min_count[minute]
                print(f"{minute}: {average_hr:.2f}")
        print("----------------------\n")
        print("Average time in each zone (Mins):")
        for zone, seconds in secs_in_zone.items():
            print(f"{zone}: {seconds / data_class_counter / 60:.2f}")
        print("----------------------\n")
    else:
        print("No workout summaries available for the selected date range.")

    # Plot average HR by minute (with enhancements)
    plt.figure(figsize=(10, 6))
    plt.plot(
        hr_totals.keys(),
        [hr_totals[min] / min_count[min] for min in hr_totals],
        label="Average HR",
    )
    plt.xlabel("Minute")
    plt.ylabel("Average Heart Rate")
    plt.title("Average HR by Minute")
    plt.grid(True)
    plt.legend()

    if hr_totals:
        plt.show()
    else:
        print("No heart rate data available for plotting.")


# Main function to drive the program
def main():
    email, password = get_credentials()
    token = get_token(email, password)
    response_data = get_in_studio_response(token)

    if "data" in response_data:
        year_input = input("Enter a year (YYYY) or leave blank for all classes: ")
        if year_input:
            start_date = datetime(int(year_input), 1, 1)
            end_date = datetime(int(year_input), 12, 31)
            processed_data = process_workouts(
                response_data["data"], token, start_date, end_date
            )
        else:
            processed_data = process_workouts(response_data["data"], token)
        print_workout_stats(*processed_data)
    else:
        print("No data found.")


if __name__ == "__main__":
    main()
