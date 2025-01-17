import calendar
from datetime import datetime
import pandas as pd
from otf_api import Otf


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

    def analyze_studio_patterns(self, performance_df):
        """
        Analyze studio attendance patterns over time.
        Args:
            performance_df: DataFrame containing workout performance data
        Returns:
            Dictionary containing studio analysis metrics
        """
        # Get unique studios and visit counts
        studio_visits = performance_df['studio'].value_counts()
        
        # Calculate first visit to each studio
        first_visits = performance_df.groupby('studio')['date'].min()
        
        # Calculate monthly studio attendance
        monthly_attendance = (
            performance_df.set_index('date')
            .groupby([pd.Grouper(freq='ME'), 'studio'])
            .size()
            .unstack(fill_value=0)
        )
        
        # Calculate year-by-year studio counts
        yearly_unique_studios = (
            performance_df.groupby(performance_df['date'].dt.year)['studio']
            .nunique()
        )
        
        return {
            'total_unique_studios': len(performance_df['studio'].unique()),
            'visits_per_studio': studio_visits.to_dict(),
            'first_visit_dates': first_visits.to_dict(),
            'monthly_attendance': monthly_attendance,
            'yearly_unique_studios': yearly_unique_studios.to_dict(),
            'most_visited_studio': studio_visits.index[0],
            'most_visits_count': studio_visits.iloc[0]
        }


    async def close(self):
        """Close the OTF client session"""
        await self.otf._session.close()
