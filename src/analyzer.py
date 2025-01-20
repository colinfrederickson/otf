import logging
from datetime import datetime
import pandas as pd
from otf_api import Otf
from pydantic import Field
from fastapi import HTTPException
from otf_api.models.base import OtfItemBase

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TotalClasses(OtfItemBase):
    total_in_studio_classes_attended: int = Field(..., alias="totalInStudioClassesAttended")
    total_otlive_classes_attended: int = Field(..., alias="totalOtliveClassesAttended")

class OTFAnalytics:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.otf = Otf(email, password)

    async def get_workout_data(self, limit=None):
        """Get detailed workout data"""
        try:
            logger.info(f"Requesting performance summaries with limit: {limit}")
            summaries = await self.otf.get_performance_summaries(limit=limit)
            
            logger.info(f"Retrieved {len(summaries.summaries)} workout summaries")
            
            if summaries.summaries:
                first_date = summaries.summaries[0].otf_class.starts_at_local
                last_date = summaries.summaries[-1].otf_class.starts_at_local
                logger.info(f"Data range: {first_date} to {last_date}")
            
            return summaries.summaries

        except Exception as e:
            logger.error(f"Error fetching workout data: {e}")
            raise HTTPException(status_code=500, detail=f"Error fetching workout data: {str(e)}")

    async def get_class_data(self):
        """Get total class attendance data"""
        try:
            logger.info("Requesting total classes data")
            total_classes = await self.otf.get_total_classes()
            logger.info(f"Raw total classes response: {total_classes}")

            # Handle string response
            if isinstance(total_classes, str):
                logger.info("Processing string response")
                class_data = {}
                for item in total_classes.split():
                    key, value = item.split('=')
                    class_data[key] = int(value)
                
                return {
                    "total_in_studio_classes": class_data.get('total_in_studio_classes_attended', 0),
                    "total_otlive_classes": class_data.get('total_otlive_classes_attended', 0)
                }
            
            # Handle model response
            if hasattr(total_classes, 'total_in_studio_classes_attended'):
                return {
                    "total_in_studio_classes": total_classes.total_in_studio_classes_attended,
                    "total_otlive_classes": total_classes.total_otlive_classes_attended
                }
                
            logger.error(f"Unexpected response format: {total_classes}")
            raise HTTPException(
                status_code=500,
                detail="Unexpected response format from OTF API"
            )

        except Exception as e:
            logger.error(f"Error fetching class data: {e}")
            raise HTTPException(status_code=500, detail=f"Error fetching class data: {str(e)}")

    async def analyze_performance(self, workouts):
        """Analyze detailed performance metrics"""
        performance_data = []
        for workout in workouts:
            try:
                detail = await self.otf.get_performance_summary(workout.id)
                performance_data.append(detail)
            except Exception as e:
                logger.warning(f"Error processing workout {workout.id}: {e}")
                continue

        return performance_data

    def analyze_studio_patterns(self, workouts):
        """Analyze studio attendance patterns"""
        try:
            studio_data = [
                {
                    'date': datetime.fromisoformat(w.otf_class.starts_at_local),
                    'studio': getattr(w.otf_class.studio, 'name', 'Unknown')
                }
                for w in workouts
            ]

            df = pd.DataFrame(studio_data)
            studio_visits = df['studio'].value_counts()
            first_visits = df.groupby('studio')['date'].min()

            return {
                "total_unique_studios": len(df['studio'].unique()),
                "visits_per_studio": studio_visits.to_dict(),
                "first_visit_dates": first_visits.to_dict(),
                "most_visited_studio": studio_visits.idxmax() if not studio_visits.empty else "Unknown",
                "most_visits_count": studio_visits.max() if not studio_visits.empty else 0
            }
        except Exception as e:
            logger.error(f"Error analyzing studio patterns: {e}")
            raise HTTPException(status_code=500, detail=f"Error analyzing studio patterns: {str(e)}")

    async def close(self):
        """Close the OTF client session"""
        try:
            await self.otf.session.close()
        except Exception as e:
            logger.error(f"Error closing session: {e}")