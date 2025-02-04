from fastapi import APIRouter, Depends, HTTPException
from api.core.config import logger
from api.core.auth import oauth2_scheme, decode_token, get_otf_client
from api.models.schemas import MemberDetailResponse, MemberDetail, WorkoutStats, StudioInfo

router = APIRouter()

@router.get("/member-detail", response_model=MemberDetailResponse)
async def get_member_detail(token: str = Depends(oauth2_scheme)):
    """Get member profile information"""
    otf = None
    try:
        credentials = decode_token(token)
        otf = await get_otf_client(credentials)
        member_detail = await otf.get_member_detail()
        
        # Debug logs
        logger.info(f"Member Class Summary: {member_detail.member_class_summary}")
        logger.info(f"Home Studio: {member_detail.home_studio}")
        logger.info(f"Max HR: {member_detail.max_hr}")
        
        # Calculate rates
        attendance_rate = (
            member_detail.member_class_summary.total_classes_attended / 
            member_detail.member_class_summary.total_classes_booked * 100
        ) if member_detail.member_class_summary.total_classes_booked > 0 else 0
        
        hrm_usage_rate = (
            member_detail.member_class_summary.total_classes_used_hrm / 
            member_detail.member_class_summary.total_classes_attended * 100
        ) if member_detail.member_class_summary.total_classes_attended > 0 else 0

        # Create response with explicit error handling
        try:
            response_data = MemberDetail(
                # Basic Info
                first_name=member_detail.first_name,
                last_name=member_detail.last_name,
                email=member_detail.email,
                
                # Fitness Profile
                max_hr=member_detail.max_hr,
                
                # Stats
                workout_stats=WorkoutStats(
                    total_classes_booked=member_detail.member_class_summary.total_classes_booked,
                    total_classes_attended=member_detail.member_class_summary.total_classes_attended,
                    total_classes_with_hrm=member_detail.member_class_summary.total_classes_used_hrm,
                    attendance_rate=round(attendance_rate, 1),
                    hrm_usage_rate=round(hrm_usage_rate, 1),
                    first_class_date=member_detail.member_class_summary.first_visit_date,
                    last_class_date=member_detail.member_class_summary.last_class_visited_date
                ),
                studio_info=StudioInfo(
                    home_studio_name=member_detail.home_studio.studio_name,
                    total_studios_visited=member_detail.member_class_summary.total_studios_visited,
                    time_zone=member_detail.home_studio.time_zone
                )
            )
            logger.info(f"Response Data: {response_data}")
            return MemberDetailResponse(status="success", data=response_data)
            
        except Exception as model_error:
            logger.error(f"Error creating response model: {str(model_error)}")
            raise HTTPException(status_code=500, detail=f"Error creating response: {str(model_error)}")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if otf and hasattr(otf, 'session') and otf.session:
            await otf.session.close()