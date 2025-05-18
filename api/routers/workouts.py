from fastapi import APIRouter, Depends, HTTPException
from api.core.config import logger
from api.core.auth import oauth2_scheme, decode_token, get_otf_client
import asyncio

router = APIRouter()

@router.get("/total-classes")
async def get_total_classes(token: str = Depends(oauth2_scheme)):
    """Get total class counts and detailed HRM workout history, sorted by most recent"""
    otf = None
    try:
        credentials = decode_token(token)
        otf = await get_otf_client(credentials)

        # Fetch all workouts with a high limit
        workouts, total_classes = await asyncio.gather(
            otf.get_performance_summaries(limit=5000),  # Ensure all workouts are retrieved
            otf.get_total_classes()
        )

        # Ensure workouts are combined (if multiple arrays exist)
        all_workouts = []
        if isinstance(workouts, list):  # Check if workouts is already a list
            for category in workouts:  # Iterate over different arrays
                if hasattr(category, "summaries"):  # Check if summaries exist
                    all_workouts.extend(category.summaries)  # Add to master list
        else:
            all_workouts = workouts.summaries  # If it's just one array, use it directly

        # Sort workouts by date (most recent first)
        sorted_workouts = sorted(
            all_workouts, 
            key=lambda workout: workout.otf_class.starts_at_local if workout.otf_class else "1970-01-01T00:00:00",
            reverse=True
        )

        # Extract HRM workout details safely
        workout_details = []
        for workout in sorted_workouts:
            workout_details.append({
                "id": workout.id,
                "class_name": workout.otf_class.name if workout.otf_class and workout.otf_class.name else "Unknown Class",
                "class_type": workout.otf_class.type if workout.otf_class and workout.otf_class.type else "Unknown Type",
                "date": workout.otf_class.starts_at_local if workout.otf_class and workout.otf_class.starts_at_local else "Unknown Date",
                "coach": workout.otf_class.coach.first_name if workout.otf_class and workout.otf_class.coach else "No Coach",
                "studio": workout.otf_class.studio.name if workout.otf_class and workout.otf_class.studio else "No Studio",
                "calories_burned": workout.details.calories_burned if workout.details else 0,
                "splat_points": workout.details.splat_points if workout.details else 0,
                "active_time": workout.details.active_time_seconds if workout.details else 0,
                "zone_time": {
                    "gray": workout.details.zone_time_minutes.gray if workout.details and workout.details.zone_time_minutes else 0,
                    "blue": workout.details.zone_time_minutes.blue if workout.details and workout.details.zone_time_minutes else 0,
                    "green": workout.details.zone_time_minutes.green if workout.details and workout.details.zone_time_minutes else 0,
                    "orange": workout.details.zone_time_minutes.orange if workout.details and workout.details.zone_time_minutes else 0,
                    "red": workout.details.zone_time_minutes.red if workout.details and workout.details.zone_time_minutes else 0,
                }
            })

        return {
            "performance_data": {
                "retrieved_workouts": len(workout_details),
                "workouts": workout_details  # Sorted HRM workout history
            },
            "total_classes": {
                "in_studio": total_classes.total_in_studio_classes_attended,
                "ot_live": total_classes.total_otlive_classes_attended,
                "total": total_classes.total_in_studio_classes_attended + total_classes.total_otlive_classes_attended
            },
            "date_range": {
                "first_class": sorted_workouts[-1].otf_class.starts_at_local if sorted_workouts else "Unknown",
                "last_class": sorted_workouts[0].otf_class.starts_at_local if sorted_workouts else "Unknown"
            },
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if otf and hasattr(otf, 'session') and otf.session:
            await otf.session.close()
