import asyncio
import configparser
from src.analyzer import OTFAnalytics
from src.visualizer import OTFVisualizer
from src.data_processor import OTFDataProcessor

async def main():

    # Load configuration
    config = configparser.ConfigParser()
    config.read("config.ini")

    email = config.get("OTF", "email")
    password = config.get("OTF", "password")

    # Initialize components
    analytics = OTFAnalytics(email, password)
    visualizer = OTFVisualizer()
    data_processor = OTFDataProcessor()

    try:
        print(f"Initializing analysis for: {email}")
        
        print("Fetching workout data...")
        workouts = await analytics.get_workout_data(limit=None)

        print("Analyzing patterns...")
        freq_data = analytics.analyze_frequency(workouts)
        perf_df = await analytics.analyze_performance(workouts)
        studio_analysis = analytics.analyze_studio_patterns(perf_df)

        print("Generating insights...")
        data_processor.print_insights(freq_data, perf_df)
        
        print("\nStudio Analysis:")
        print(f"Total Unique Studios: {studio_analysis['total_unique_studios']}")
        print(f"Most Visited Studio: {studio_analysis['most_visited_studio']} ({studio_analysis['most_visits_count']} visits)")
        
        print("\nVisits per Studio:")
        for studio, visits in studio_analysis['visits_per_studio'].items():
            print(f"  {studio}: {visits} visits")

        print("\nGenerating visualizations...")
        visualizer.generate_visualizations(freq_data, perf_df)
        visualizer.generate_studio_visualizations(studio_analysis)  # You would need to add this method

        print("\nVisualization files generated:")
        print("- yearly_overview.png")
        print("- monthly_patterns.png")
        print("- performance_dashboard.png")
        print("- day_of_week_analysis.png")
        print("- studio_analysis.png")  # New visualization file

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise e

    finally:
        await analytics.close()

if __name__ == "__main__":
    asyncio.run(main())
