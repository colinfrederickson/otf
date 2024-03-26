# OrangeTheory Fitness Workout Data Analysis

A Python utility for retrieving and analyzing workout data from your OrangeTheory Fitness account.

## Features

- Retrieves workout data from the OrangeTheory Fitness API.
- Provides a comprehensive analysis of your workout history, focusing on the year 2024.
- Displays workout statistics, including:
  - Total workouts and percentage of workouts attended.
  - Breakdown of classes by type, coach, and location.
  - Personal bests for maximum speed, distance, calories, and splat points.
  - Average heart rate, time spent in each heart rate zone, and calorie burn.
  - Detailed heart rate analysis by minute.

## Prerequisites

- Python 3.x
- `requests` library

## Installation

1. Clone the repository:
git clone https://github.com/your-username/otf-workout-analysis.git


2. Install the required dependencies:
pip3 install requests


3. Create a `config.ini` file in the project directory with the following content:
[OTF]
email = your-email@example.com
password = your-password

Replace `your-email@example.com` with your OrangeTheory Fitness email and `your-password` with your account password.

## Usage

To run the script, execute the following command in the project directory:
python3 main.py

The script will retrieve your workout data from the OrangeTheory Fitness API and provide a detailed analysis of your workout history for the year 2024.

## Output

The script will display the following information:

- Total workouts and percentage of workouts attended in 2024.
- Breakdown of classes by type, coach, and location.
- Personal bests for maximum speed, distance, calories, and splat points.
- Average heart rate, time spent in each heart rate zone, and calorie burn.
- Detailed heart rate analysis by minute.

## Limitations

- The script currently focuses on workout data for the year 2024. Modify the code to analyze data for different years if needed.
- The accuracy and completeness of the analysis depend on the availability and reliability of the OrangeTheory Fitness API data.
- Some assumptions are made about the structure and availability of the data. If you encounter any errors or missing data, please create an issue on GitHub or reach out for assistance.

## Future Enhancements

- Create a Postman collection to better explore the OrangeTheory Fitness API and make it more easily accessible.
- Identify and handle data assumptions and errors arising from them.
- Retrieve and analyze challenge/benchmark data and progression.
- Utilize the pandas library for enhanced data processing and analysis.
- Generate visualizations and graphs to better represent the workout data.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please create an issue on the GitHub repository.

## Contact

For any questions or inquiries, please contact the project maintainer at cfrederickson5@gmail.com.
