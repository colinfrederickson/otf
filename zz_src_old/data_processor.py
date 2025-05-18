import pandas as pd

class OTFDataProcessor:
    @staticmethod
    def print_insights(freq_data, perf_df):
        """Print detailed insights from the data"""
        print("\n=== OTF Workout Analysis ===")

        print("\nFrequency Insights:")
        print(f"Total Classes Analyzed: {len(perf_df)}")
        print(f"Average Weekly Classes: {freq_data['avg_weekly_classes']:.1f}")

        print("\nStudio Insights:")
        unique_studios = len(perf_df['studio'].unique())
        studio_visits = perf_df['studio'].value_counts()
        print(f"Number of Unique Studios: {unique_studios}")
        print("\nVisits per Studio:")
        for studio, visits in studio_visits.items():
            print(f"  {studio}: {visits} visits")

        print("\nYearly Class Totals:")
        for year, classes in freq_data["classes_per_year"].items():
            print(f"{year}: {classes} classes")

        print("\nMonthly Averages:")
        monthly_avg = freq_data["classes_per_month"].mean()
        best_month = monthly_avg.idxmax()
        print(f"Most Active Month: {best_month} (avg: {monthly_avg[best_month]:.1f} classes)")

        print("\nPerformance Insights:")
        print(f"Average Splat Points: {perf_df['splat_points'].mean():.1f}")
        print(f"Average Calories: {perf_df['calories'].mean():.1f}")
        print(f"Average Treadmill Distance: {perf_df['tread_distance'].mean():.2f} miles")

        print("\nPersonal Records:")
        print(f"Most Splat Points: {perf_df['splat_points'].max():.0f}")
        print(f"Highest Calorie Burn: {perf_df['calories'].max():.0f}")
        print(f"Longest Treadmill Distance: {perf_df['tread_distance'].max():.2f} miles")
        print(f"Fastest Speed: {perf_df['max_speed'].max():.1f} mph")

        # Best performing days
        weekday_stats = perf_df.groupby("weekday").agg({
            "splat_points": "mean",
            "calories": "mean",
            "tread_distance": "mean"
        })

        print("\nBest Performing Days:")
        best_splat_day = weekday_stats["splat_points"].idxmax()
        best_calorie_day = weekday_stats["calories"].idxmax()
        best_distance_day = weekday_stats["tread_distance"].idxmax()
        
        print(f"Most Splat Points: {best_splat_day} ({weekday_stats.loc[best_splat_day, 'splat_points']:.1f})")
        print(f"Highest Calories: {best_calorie_day} ({weekday_stats.loc[best_calorie_day, 'calories']:.1f})")
        print(f"Best Distance: {best_distance_day} ({weekday_stats.loc[best_distance_day, 'tread_distance']:.2f} miles)")

        # Studio comparison
        print("\nStudio Performance:")
        studio_stats = perf_df.groupby("studio").agg({
            "splat_points": "mean",
            "calories": "mean",
            "tread_distance": "mean"
        })
        
        for studio in studio_stats.index:
            print(f"\n{studio}:")
            print(f"  Avg Splats: {studio_stats.loc[studio, 'splat_points']:.1f}")
            print(f"  Avg Calories: {studio_stats.loc[studio, 'calories']:.1f}")
            print(f"  Avg Distance: {studio_stats.loc[studio, 'tread_distance']:.2f} miles")


    @staticmethod
    def process_heart_rate_data(workout_details):
        """Process heart rate zone data from workout details"""
        if hasattr(workout_details, "zone_time_minutes"):
            zones = workout_details.zone_time_minutes
            return {
                "red_zone": getattr(zones, "red", 0),
                "orange_zone": getattr(zones, "orange", 0),
                "green_zone": getattr(zones, "green", 0),
                "blue_zone": getattr(zones, "blue", 0),
                "gray_zone": getattr(zones, "gray", 0),
            }
        return {
            "red_zone": 0,
            "orange_zone": 0,
            "green_zone": 0,
            "blue_zone": 0,
            "gray_zone": 0,
        }
    
    @staticmethod
    def process_equipment_data(details):
        """Process equipment data from workout details"""
        equipment_data = {
            "tread_distance": 0.0,
            "max_speed": 0.0,
            "avg_speed": 0.0,
            "rower_distance": 0.0,
        }
        
        if hasattr(details, "equipment_data"):
            equip = details.equipment_data
            
            # Process treadmill data
            if hasattr(equip, "treadmill"):
                tread = equip.treadmill
                if hasattr(tread, "total_distance"):
                    equipment_data["tread_distance"] = float(tread.total_distance.display_value)
                if hasattr(tread, "max_speed"):
                    equipment_data["max_speed"] = float(tread.max_speed.display_value)
                if hasattr(tread, "avg_speed"):
                    equipment_data["avg_speed"] = float(tread.avg_speed.display_value)
            
            # Process rower data
            if hasattr(equip, "rower"):
                rower = equip.rower
                if hasattr(rower, "total_distance"):
                    equipment_data["rower_distance"] = float(rower.total_distance.display_value)
                    
        return equipment_data
    
    @staticmethod
    def calculate_weekly_stats(perf_df):
        """Calculate weekly performance statistics"""
        weekly_stats = perf_df.resample('W', on='date').agg({
            'calories': 'sum',
            'splat_points': 'sum',
            'tread_distance': 'sum'
        })
        return weekly_stats
    
    @staticmethod
    def calculate_monthly_stats(perf_df):
        """Calculate monthly performance statistics"""
        monthly_stats = perf_df.resample('M', on='date').agg({
            'calories': 'sum',
            'splat_points': 'sum',
            'tread_distance': 'sum'
        })
        return monthly_stats