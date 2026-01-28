"""
Background removal service.
This file contains the core logic for removing backgrounds from images.
"""

from io import BytesIO
from PIL import Image
from rembg import remove
from app.config import settings


class BackgroundRemovalService:
    """
    Service class for handling background removal operations.
    Uses the rembg library which implements U²-Net deep learning model.
    """
    
    @staticmethod
    def remove_background(image_bytes: bytes) -> bytes:
        """
        Remove background from an image.
        
        Args:
            image_bytes (bytes): The input image as bytes
            
        Returns:
            bytes: The processed image with transparent background as PNG bytes
            
        How it works:
        1. Converts bytes to PIL Image
        2. Resizes if needed (to prevent memory issues)
        3. Uses rembg to remove background
        4. Returns PNG with transparency
        """
        
        # Step 1: Load the image from bytes
        input_image = Image.open(BytesIO(image_bytes))
        
        # Step 2: Resize if the image is too large
        # This prevents memory issues and speeds up processing
        if input_image.width > settings.MAX_IMAGE_WIDTH:
            # Calculate new height to maintain aspect ratio
            ratio = settings.MAX_IMAGE_WIDTH / input_image.width
            new_height = int(input_image.height * ratio)
            
            # Resize using high-quality Lanczos algorithm
            input_image = input_image.resize(
                (settings.MAX_IMAGE_WIDTH, new_height),
                Image.Resampling.LANCZOS
            )
        
        # Step 3: Remove background using rembg
        # The remove() function uses a pre-trained U²-Net model
        # It automatically detects the main subject and removes the background
        output_image = remove(input_image)
        
        # Step 4: Convert to bytes for HTTP response
        output_buffer = BytesIO()
        output_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)  # Reset buffer position to the beginning
        
        return output_buffer.getvalue()
    
    @staticmethod
    def validate_image(image_bytes: bytes, filename: str) -> tuple[bool, str]:
        """
        Validate uploaded image file.
        
        Args:
            image_bytes (bytes): The image file bytes
            filename (str): The original filename
            
        Returns:
            tuple[bool, str]: (is_valid, error_message)
                - is_valid: True if valid, False otherwise
                - error_message: Description of the error, empty string if valid
        """
        
        # Check 1: File size validation
        file_size_mb = len(image_bytes) / (1024 * 1024)
        if len(image_bytes) > settings.MAX_FILE_SIZE_BYTES:
            return False, f"File too large. Maximum size is {settings.MAX_FILE_SIZE_MB}MB, got {file_size_mb:.2f}MB"
        
        # Check 2: File extension validation
        file_extension = filename.lower()[filename.rfind('.'):]
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            allowed = ", ".join(settings.ALLOWED_EXTENSIONS)
            return False, f"Invalid file type. Allowed types: {allowed}"
        
        # Check 3: Try to open the image to verify it's valid
        try:
            image = Image.open(BytesIO(image_bytes))
            image.verify()  # Verify that it's actually an image
            return True, ""
        except Exception as e:
            return False, f"Invalid or corrupted image file: {str(e)}"


# Create a global service instance
bg_service = BackgroundRemovalService()