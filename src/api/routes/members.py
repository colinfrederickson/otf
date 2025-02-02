from fastapi import APIRouter, HTTPException, Depends
from ..models.schemas import MemberDetailResponse
from ..core.auth import get_current_user, get_otf_client
from ..core.logging import logger

router = APIRouter()

@router.get("/api/member-detail")  # Keep the old endpoint path
async def get_member_detail(credentials: dict = Depends(get_current_user)):
    """Get member details - legacy endpoint"""
    return await _get_member_detail(credentials)

@router.get("/api/members/detail")  # New endpoint path
async def get_member_detail_new(credentials: dict = Depends(get_current_user)):
    """Get member details - new endpoint"""
    return await _get_member_detail(credentials)

async def _get_member_detail(credentials: dict):
    """Shared implementation for both endpoints"""
    otf = None
    try:
        otf = await get_otf_client(credentials)
        member_detail = await otf.get_member_detail()
        
        return MemberDetailResponse(
            status="success",
            data={
                "first_name": member_detail.first_name,
                "last_name": member_detail.last_name,
                "user_name": member_detail.user_name,
                "email": member_detail.email,
            }
        )
        
    except Exception as e:
        logger.error(f"Error fetching member detail: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch member detail")
    finally:
        if otf and otf.session:
            await otf.session.close()