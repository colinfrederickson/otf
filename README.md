# OrangeTheory Fitness Analytics Tool

A comprehensive web application for analyzing and visualizing workout data from your OrangeTheory Fitness account.

## Features

- **Secure Login**:

  - Token-based authentication for secure access.
  - User-specific data retrieval after login.

- **Dashboard**:

  - Overview of total class attendance.
  - Detailed performance metrics, including:
    - In-studio and OTF Live class breakdown.

- **Data Retrieval and Analysis**:
  - Advanced data retrieval from the OrangeTheory Fitness API.
  - Comprehensive performance analytics:
    - Workout frequency patterns.
    - Studio-specific attendance trends.
    - Performance trends over time.

### API Features

- `/api/login`: Authenticate users and issue tokens.
- `/api/total-classes`: Retrieve class attendance and performance data.
- Future endpoints to expand data visualization and user analytics.

## Prerequisites

- Node.js and npm for running the web application.
- A modern web browser for accessing the app.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/otf-analytics.git
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Create a `.env` file for configuration:

   ```env
   REACT_APP_API_URL=http://localhost:8000/api
   ```

4. Start the development server:

   ```bash
   npm start
   ```

5. Set up the backend by running the Python server (API):
   - Install the required Python packages:
     ```bash
     pip install fastapi uvicorn pandas requests
     ```
   - Start the backend server:
     ```bash
     uvicorn api.main:app --reload
     ```

## Usage

1. Open the web app in your browser (default: `http://localhost:3000`).
2. Log in using your OrangeTheory Fitness credentials.
3. Access the dashboard to view:
   - Total class attendance.
   - Performance metrics and trends.

## Analysis Features

### Dashboard Overview

- Total classes attended.
- Breakdown of in-studio vs. OTF Live classes.

## Future Development

- Integration of workout visualizations.
- Enhanced performance trend analysis.
- Benchmark and personal records tracking.
- User-specific goal setting and tracking.
- Mobile-friendly responsive design.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

## Contact

Project maintainer: [cfrederickson5@gmail.com](mailto:cfrederickson5@gmail.com)
