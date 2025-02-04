from fastapi import APIRouter, Depends, HTTPException
from api.core.config import logger
from api.core.auth import oauth2_scheme, decode_token, get_otf_client
import asyncio

router = APIRouter()

@router.get("/total-classes")
async def get_total_classes(token: str = Depends(oauth2_scheme)):
    """Get total class counts and workout history"""
    otf = None
    try:
        credentials = decode_token(token)
        otf = await get_otf_client(credentials)
        
        # Get data in parallel
        workouts, total_classes = await asyncio.gather(
            otf.get_performance_summaries(limit=None),
            otf.get_total_classes()
        )
        
        return {
            "performance_data": {
                "retrieved_workouts": len(workouts.summaries)
            },
            "total_classes": {
                "in_studio": total_classes.total_in_studio_classes_attended,
                "ot_live": total_classes.total_otlive_classes_attended,
                "total": total_classes.total_in_studio_classes_attended + total_classes.total_otlive_classes_attended
            },
            "date_range": {
                "first_class": workouts.summaries[0].otf_class.starts_at_local,
                "last_class": workouts.summaries[-1].otf_class.starts_at_local
            } if workouts.summaries else None,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if otf and hasattr(otf, 'session') and otf.session:
            await otf.session.close()