"""
Router for background removal endpoints.
This file defines the API routes for image processing.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO

from app.services.bg_service import bg_service


# Create a router instance
# prefix="/api" means all routes here will start with /api
router = APIRouter(
    prefix="/api",
    tags=["Background Removal"]  # Groups endpoints in API docs
)


@router.post(
    "/remove-bg",
    summary="Remove background from image",
    description="""
    Upload an image and get back the same image with the background removed.
    
    **Accepted formats:** JPG, PNG
    **Max file size:** 5MB
    **Returns:** PNG image with transparent background
    """
)
async def remove_background(
    file: UploadFile = File(
        ...,
        description="Image file to process (JPG or PNG)"
    )
):
    """
    Remove background from uploaded image.
    
    This endpoint:
    1. Receives an image file
    2. Validates file type and size
    3. Processes it to remove background
    4. Returns PNG with transparent background
    
    Args:
        file (UploadFile): The uploaded image file
        
    Returns:
        StreamingResponse: PNG image with transparent background
        
    Raises:
        HTTPException: If validation fails or processing errors occur
    """
    
    try:
        # Step 1: Read the uploaded file
        image_bytes = await file.read()
        
        # Step 2: Validate the image
        is_valid, error_message = bg_service.validate_image(image_bytes, file.filename)
        
        if not is_valid:
            # Return HTTP 400 Bad Request with error details
            raise HTTPException(status_code=400, detail=error_message)
        
        # Step 3: Process the image (remove background)
        output_bytes = bg_service.remove_background(image_bytes)
        
        # Step 4: Return the processed image
        # StreamingResponse allows us to return binary data (image)
        return StreamingResponse(
            BytesIO(output_bytes),
            media_type="image/png",
            headers={
                "Content-Disposition": f"attachment; filename=no_bg_{file.filename.rsplit('.', 1)[0]}.png"
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    
    except Exception as e:
        # Catch any unexpected errors during processing
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )


@router.get(
    "/health",
    summary="Health check",
    description="Check if the API is running properly"
)
async def health_check():
    """
    Simple health check endpoint.
    Returns status information about the API.
    """
    return {
        "status": "healthy",
        "message": "Background Remover API is running",
        "version": "1.0.0"
    }