import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class OTFVisualizer:
    def __init__(self):
        self.colors = ["#f58220", "#1e88e5", "#43a047", "#e53935", "#5e35b1"]
        plt.style.use("default")

    def generate_visualizations(self, freq_data, perf_df):
        """Generate all visualizations"""
        self._generate_yearly_overview(freq_data)
        self._generate_monthly_patterns(freq_data)
        self._generate_performance_dashboard(perf_df)
        self._generate_day_analysis(perf_df)

    def generate_studio_visualizations(self, studio_analysis):
        """Generate studio analysis visualizations"""
        self._generate_studio_visits(studio_analysis)
        self._generate_studio_monthly_attendance(studio_analysis)
        self._generate_studio_yearly_analysis(studio_analysis)

    def generate_challenge_visualizations(self, challenge_data):
        """Generate challenge-related visualizations"""
        self._generate_benchmark_progress(challenge_data['details'])
        self._generate_challenge_participation(challenge_data['challenges'])

    def _generate_yearly_overview(self, freq_data):
        """Generate yearly overview visualization"""
        plt.figure(figsize=(12, 6))
        freq_data["classes_per_year"].plot(kind="bar", color=self.colors[0])
        plt.title("Classes per Year", fontsize=14, pad=20)
        plt.xlabel("Year")
        plt.ylabel("Number of Classes")
        plt.grid(True, axis="y", alpha=0.3)
        plt.tight_layout()
        plt.savefig("yearly_overview.png")
        plt.close()

    def _generate_monthly_patterns(self, freq_data):
        """Generate monthly patterns visualization"""
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

    def _generate_performance_dashboard(self, perf_df):
        """Generate performance dashboard visualization"""
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
        axes[0, 1].pie(zone_avgs, labels=zone_cols, colors=self.colors, autopct="%1.1f%%")
        axes[0, 1].set_title("Average Time in Zones")

        # Distance Trends
        perf_df.plot(x="date", y="tread_distance", ax=axes[1, 0], color=self.colors[2])
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

    def _generate_day_analysis(self, perf_df):
        """Generate day of week analysis visualization"""
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

    def _generate_studio_visits(self, studio_analysis):
        """Generate studio visits visualization"""
        plt.figure(figsize=(15, 8))
        visits = pd.Series(studio_analysis['visits_per_studio'])
        visits.sort_values(ascending=True).plot(kind='barh', color=self.colors[0])
        plt.title('Total Visits by Studio', fontsize=14, pad=20)
        plt.xlabel('Number of Visits')
        plt.ylabel('Studio')
        plt.grid(True, axis='x', alpha=0.3)
        plt.tight_layout()
        plt.savefig('studio_visits.png')
        plt.close()

    def _generate_studio_monthly_attendance(self, studio_analysis):
        """Generate monthly attendance patterns by studio"""
        if 'monthly_attendance' in studio_analysis:
            plt.figure(figsize=(15, 8))
            studio_analysis['monthly_attendance'].plot(kind='area', stacked=True)
            plt.title('Monthly Studio Attendance Pattern', fontsize=14, pad=20)
            plt.xlabel('Date')
            plt.ylabel('Number of Visits')
            plt.legend(title='Studio', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig('studio_monthly_pattern.png')
            plt.close()

    def _generate_studio_yearly_analysis(self, studio_analysis):
        """Generate yearly studio analysis visualization"""
        if 'yearly_unique_studios' in studio_analysis:
            plt.figure(figsize=(10, 6))
            yearly_studios = pd.Series(studio_analysis['yearly_unique_studios'])
            yearly_studios.plot(kind='bar', color=self.colors[1])
            plt.title('Unique Studios Visited per Year', fontsize=14, pad=20)
            plt.xlabel('Year')
            plt.ylabel('Number of Unique Studios')
            plt.grid(True, axis='y', alpha=0.3)
            plt.tight_layout()
            plt.savefig('yearly_studios.png')
            plt.close()
