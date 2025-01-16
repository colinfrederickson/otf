# OrangeTheory Fitness Analytics Tool

A comprehensive Python utility for analyzing and visualizing workout data from your OrangeTheory Fitness account.

## Features

- Advanced data retrieval and analysis from the OrangeTheory Fitness API
- Comprehensive performance analytics including:
  - Workout frequency patterns
  - Performance trends over time
  - Heart rate zone analysis
  - Equipment performance tracking (treadmill, rower)
  - Studio and coach comparisons
  - Personal records tracking

### Visualizations

- Yearly workout overview
- Monthly attendance patterns
- Performance dashboard
- Day-of-week analysis

### Analytics

- Detailed performance metrics
- Studio-specific performance analysis
- Time-based trending
- Comprehensive heart rate zone analysis
- Equipment-specific performance tracking

## Prerequisites

- Python 3.x
- Required packages:
  ```bash
  pip install otf-api pandas matplotlib configparser
  ```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/otf-analytics.git
   ```

2. Create a `config.ini` file:
   ```ini
   [OTF]
   email = your-otf-email@example.com
   password = your-otf-password
   ```

## Usage

Run the analysis:

```bash
python3 main.py
```

## Output Files

The script generates several visualization files:

- `yearly_overview.png`
- `monthly_patterns.png`
- `performance_dashboard.png`
- `day_of_week_analysis.png`

## Analysis Features

### Frequency Analysis

- Classes per year
- Monthly patterns
- Weekly averages
- Day-of-week trends

### Performance Metrics

- Splat points and calories
- Distance and speed records
- Heart rate zone distribution
- Studio performance comparison

### Personal Records

- Speed and distance
- Calorie burn
- Splat points
- Zone achievements

## Future Development

- Enhanced benchmark tracking
- Advanced performance analytics
- Year-over-year comparisons
- Workout type analysis
- Custom performance scores

## Contributing

Contributions are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

## Contact

Project maintainer: [cfrederickson5@gmail.com](mailto:cfrederickson5@gmail.com)
