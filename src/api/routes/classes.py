from fastapi import APIRouter, HTTPException, Depends
import asyncio
from ..models.schemas import ClassesResponse, PerformanceData, TotalClasses, DateRange
from ..core.auth import get_current_user, get_otf_client
from ..core.logging import logger

router = APIRouter()  # Remove prefix

# Add both endpoint paths
@router.get("/api/total-classes")  # Original path
@router.get("/api/classes/total")  # New path
async def get_total_classes(credentials: dict = Depends(get_current_user)):
    otf = None
    try:
        otf = await get_otf_client(credentials)
        
        # Get data in parallel
        workouts, total_classes = await asyncio.gather(
            otf.get_performance_summaries(limit=None),
            otf.get_total_classes()
        )
        
        response_data = {
            "performance_data": PerformanceData(
                retrieved_workouts=len(workouts.summaries)
            ),
            "total_classes": TotalClasses(
                in_studio=total_classes.total_in_studio_classes_attended,
                ot_live=total_classes.total_otlive_classes_attended,
                total=total_classes.total_in_studio_classes_attended + total_classes.total_otlive_classes_attended
            ),
            "status": "success",
            "message": "Data retrieved successfully"
        }

        if workouts.summaries:
            response_data["date_range"] = DateRange(
                first_class=workouts.summaries[0].otf_class.starts_at_local,
                last_class=workouts.summaries[-1].otf_class.starts_at_local
            )
        
        return ClassesResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error retrieving class data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while retrieving class data"
        )
    finally:
        if otf and otf.session:
            await otf.session.close()