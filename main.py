import asyncio
import configparser
from otf_api import Otf
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import calendar


class OTFAnalytics:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.otf = Otf(email, password)

    async def get_workout_data(self, limit=100):
        """Get detailed workout data"""
        summaries = await self.otf.get_performance_summaries(limit=limit)
        return summaries.summaries

    def analyze_frequency(self, workouts):
        """Analyze workout frequency patterns"""
        dates = [datetime.fromisoformat(w.otf_class.starts_at_local) for w in workouts]
        df = pd.DataFrame({"date": dates})
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["day"] = df["date"].dt.day
        df["weekday"] = df["date"].dt.strftime("%A")

        # Classes per year
        classes_per_year = df.groupby("year").size()

        # Classes per month per year
        classes_per_month = df.groupby(["year", "month"]).size().unstack(fill_value=0)
        classes_per_month.columns = [
            calendar.month_abbr[m] for m in classes_per_month.columns
        ]

        # Average classes per week
        weekly_classes = df.resample("W", on="date").size().mean()

        return {
            "classes_per_year": classes_per_year,
            "classes_per_month": classes_per_month,
            "avg_weekly_classes": weekly_classes,
        }

    async def analyze_performance(self, workouts):
        """Analyze detailed performance metrics"""
        performance_data = []

        for workout in workouts:
            date = datetime.fromisoformat(workout.otf_class.starts_at_local)
            detail = await self.otf.get_performance_summary(workout.id)

            # Base workout data
            workout_data = {
                "date": date,
                "weekday": date.strftime("%A"),
                "time": date.strftime("%H:%M"),
                "calories": workout.details.calories_burned,
                "splat_points": workout.details.splat_points,
                "type": workout.otf_class.name,
                "studio": (
                    workout.otf_class.studio.name
                    if hasattr(workout.otf_class.studio, "name")
                    else "Unknown"
                ),
                "coach": (
                    workout.otf_class.coach.name
                    if hasattr(workout.otf_class.coach, "name")
                    else "Unknown"
                ),
            }

            # Add heart rate zones
            if hasattr(workout.details, "zone_time_minutes"):
                zones = workout.details.zone_time_minutes
                workout_data.update(
                    {
                        "red_zone": getattr(zones, "red", 0),
                        "orange_zone": getattr(zones, "orange", 0),
                        "green_zone": getattr(zones, "green", 0),
                        "blue_zone": getattr(zones, "blue", 0),
                        "gray_zone": getattr(zones, "gray", 0),
                    }
                )
            else:
                workout_data.update(
                    {
                        "red_zone": 0,
                        "orange_zone": 0,
                        "green_zone": 0,
                        "blue_zone": 0,
                        "gray_zone": 0,
                    }
                )

            # Add equipment data
            workout_data.update(
                {
                    "tread_distance": 0.0,
                    "max_speed": 0.0,
                    "avg_speed": 0.0,
                    "rower_distance": 0.0,
                }
            )

            if hasattr(detail.details, "equipment_data"):
                equip = detail.details.equipment_data

                # Treadmill data
                if hasattr(equip, "treadmill"):
                    tread = equip.treadmill
                    if hasattr(tread, "total_distance"):
                        workout_data["tread_distance"] = float(
                            tread.total_distance.display_value
                        )
                    if hasattr(tread, "max_speed"):
                        workout_data["max_speed"] = float(tread.max_speed.display_value)
                    if hasattr(tread, "avg_speed"):
                        workout_data["avg_speed"] = float(tread.avg_speed.display_value)

                # Rower data
                if hasattr(equip, "rower"):
                    rower = equip.rower
                    if hasattr(rower, "total_distance"):
                        workout_data["rower_distance"] = float(
                            rower.total_distance.display_value
                        )

            performance_data.append(workout_data)

        return pd.DataFrame(performance_data)

    def generate_visualizations(self, freq_data, perf_df):
        """Generate comprehensive visualizations"""
        # Set plot style
        plt.style.use("default")
        colors = ["#f58220", "#1e88e5", "#43a047", "#e53935", "#5e35b1"]

        # 1. Yearly Overview
        plt.figure(figsize=(12, 6))
        freq_data["classes_per_year"].plot(kind="bar", color=colors[0])
        plt.title("Classes per Year", fontsize=14, pad=20)
        plt.xlabel("Year")
        plt.ylabel("Number of Classes")
        plt.grid(True, axis="y", alpha=0.3)
        plt.tight_layout()
        plt.savefig("yearly_overview.png")
        plt.close()

        # 2. Monthly Patterns
        plt.figure(figsize=(15, 7))
        freq_data["classes_per_month"].plot(kind="bar", stacked=False)
        plt.title("Classes per Month by Year", fontsize=14, pad=20)
        plt.xlabel("Year")
        plt.ylabel("Number of Classes")
        plt.legend(title="Month", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(True, axis="y", alpha=0.3)
        plt.tight_layout()
        plt.savefig("monthly_patterns.png")
        plt.close()

        # 3. Performance Dashboard
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle("Performance Dashboard", fontsize=16, y=0.95)

        # Splat Points and Calories
        perf_df.plot(x="date", y=["splat_points", "calories"], ax=axes[0, 0])
        axes[0, 0].set_title("Splat Points and Calories")
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].set_xlabel("Date")

        # Zone Distribution
        zone_cols = ["red_zone", "orange_zone", "green_zone", "blue_zone", "gray_zone"]
        zone_avgs = perf_df[zone_cols].mean()
        axes[0, 1].pie(zone_avgs, labels=zone_cols, colors=colors, autopct="%1.1f%%")
        axes[0, 1].set_title("Average Time in Zones")

        # Distance Trends
        perf_df.plot(x="date", y="tread_distance", ax=axes[1, 0], color=colors[2])
        axes[1, 0].set_title("Treadmill Distance")
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].set_xlabel("Date")
        axes[1, 0].set_ylabel("Miles")

        # Speed Progress
        perf_df.plot(x="date", y=["max_speed", "avg_speed"], ax=axes[1, 1])
        axes[1, 1].set_title("Speed Progression")
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].set_xlabel("Date")
        axes[1, 1].set_ylabel("MPH")

        plt.tight_layout()
        plt.savefig("performance_dashboard.png")
        plt.close()

        # 4. Day of Week Analysis
        plt.figure(figsize=(12, 6))
        day_stats = perf_df.groupby("weekday").agg(
            {"splat_points": "mean", "calories": "mean", "tread_distance": "mean"}
        )
        # Reorder days
        day_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        day_stats = day_stats.reindex(day_order)

        # Scale calories to fit on same plot
        day_stats["calories"] = day_stats["calories"] / 10

        day_stats.plot(kind="bar", width=0.8)
        plt.title("Performance by Day of Week", fontsize=14, pad=20)
        plt.xlabel("Day")
        plt.ylabel("Value")
        plt.legend(["Splat Points", "Calories (÷10)", "Distance (miles)"])
        plt.grid(True, axis="y", alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("day_of_week_analysis.png")
        plt.close()

    def print_insights(self, freq_data, perf_df):
        """Print detailed insights from the data"""
        print("\n=== OTF Workout Analysis ===")

        print("\nFrequency Insights:")
        print(f"Total Classes Analyzed: {len(perf_df)}")
        print(f"Average Weekly Classes: {freq_data['avg_weekly_classes']:.1f}")

        print("\nYearly Class Totals:")
        for year, classes in freq_data["classes_per_year"].items():
            print(f"{year}: {classes} classes")

        print("\nMonthly Averages:")
        monthly_avg = freq_data["classes_per_month"].mean()
        best_month = monthly_avg.idxmax()
        print(
            f"Most Active Month: {best_month} (avg: {monthly_avg[best_month]:.1f} classes)"
        )

        print("\nPerformance Insights:")
        print(f"Average Splat Points: {perf_df['splat_points'].mean():.1f}")
        print(f"Average Calories: {perf_df['calories'].mean():.1f}")
        print(
            f"Average Treadmill Distance: {perf_df['tread_distance'].mean():.2f} miles"
        )

        print("\nPersonal Records:")
        print(f"Most Splat Points: {perf_df['splat_points'].max():.0f}")
        print(f"Highest Calorie Burn: {perf_df['calories'].max():.0f}")
        print(
            f"Longest Treadmill Distance: {perf_df['tread_distance'].max():.2f} miles"
        )
        print(f"Fastest Speed: {perf_df['max_speed'].max():.1f} mph")

        # Best performing days
        weekday_stats = perf_df.groupby("weekday").agg(
            {"splat_points": "mean", "calories": "mean", "tread_distance": "mean"}
        )
        print("\nBest Performing Days:")
        best_splat_day = weekday_stats["splat_points"].idxmax()
        best_calorie_day = weekday_stats["calories"].idxmax()
        best_distance_day = weekday_stats["tread_distance"].idxmax()
        print(
            f"Most Splat Points: {best_splat_day} ({weekday_stats.loc[best_splat_day, 'splat_points']:.1f})"
        )
        print(
            f"Highest Calories: {best_calorie_day} ({weekday_stats.loc[best_calorie_day, 'calories']:.1f})"
        )
        print(
            f"Best Distance: {best_distance_day} ({weekday_stats.loc[best_distance_day, 'tread_distance']:.2f} miles)"
        )

        # Studio comparison
        print("\nStudio Performance:")
        studio_stats = perf_df.groupby("studio").agg(
            {"splat_points": "mean", "calories": "mean", "tread_distance": "mean"}
        )
        for studio in studio_stats.index:
            print(f"\n{studio}:")
            print(f"  Avg Splats: {studio_stats.loc[studio, 'splat_points']:.1f}")
            print(f"  Avg Calories: {studio_stats.loc[studio, 'calories']:.1f}")
            print(
                f"  Avg Distance: {studio_stats.loc[studio, 'tread_distance']:.2f} miles"
            )


async def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    email = config.get("OTF", "email")
    password = config.get("OTF", "password")

    print(f"Initializing analysis for: {email}")
    analytics = OTFAnalytics(email, password)

    try:
        print("Fetching workout data...")
        workouts = await analytics.get_workout_data(limit=100)

        print("Analyzing patterns...")
        freq_data = analytics.analyze_frequency(workouts)
        perf_df = await analytics.analyze_performance(workouts)

        print("Generating insights and visualizations...")
        analytics.print_insights(freq_data, perf_df)
        analytics.generate_visualizations(freq_data, perf_df)

        print("\nVisualization files generated:")
        print("- yearly_overview.png")
        print("- monthly_patterns.png")
        print("- performance_dashboard.png")
        print("- day_of_week_analysis.png")

    finally:
        await analytics.otf._session.close()


if __name__ == "__main__":
    asyncio.run(main())
