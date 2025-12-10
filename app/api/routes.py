"""
API routes for file conversion.
Defines all HTTP endpoints for the application.
"""

import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from app.config import settings
from app.utils.validators import (
    validate_file_size,
    validate_file_format,
    validate_output_format,
    sanitize_filename
)
from app.services.file_handler import file_handler
from app.services.converter import cloudconvert_service, ConversionError

router = APIRouter()


@router.get("/api/health")
async def health_check():
    """Health check endpoint."""
    api_configured = bool(
        settings.cloudconvert_api_key and 
        settings.cloudconvert_api_key != "your_api_key_here"
    )
    
    return {
        "status": "healthy",
        "api_configured": api_configured,
        "supported_formats": settings.supported_formats,
        "max_file_size_mb": settings.max_file_size_mb
    }


@router.get("/api/formats")
async def get_supported_formats():
    """Get list of supported file formats."""
    return {
        "input_formats": settings.supported_formats,
        "output_formats": settings.supported_formats
    }


@router.post("/api/convert")
async def convert_file(
    file: UploadFile = File(...),
    output_format: str = Form(...)
):
    """
    Convert an uploaded image file to a different format.
    
    Args:
        file: The image file to convert
        output_format: Desired output format (jpeg, png, webp, gif)
        
    Returns:
        Information about the conversion and download URL
    """
    input_file_path = None
    output_file_path = None
    
    try:
        # Validate file size
        validate_file_size(file)
        
        # Validate input format
        input_format = validate_file_format(file.filename)
        
        # Validate output format
        output_format = validate_output_format(output_format)
        
        # Check if conversion is needed
        if input_format == output_format:
            # Normalize jpg/jpeg
            if not (input_format in ['jpg', 'jpeg'] and output_format in ['jpg', 'jpeg']):
                return {
                    "success": False,
                    "error": f"File is already in {output_format} format"
                }
        
        # Save uploaded file
        input_file_path = await file_handler.save_upload(file)
        
        # Generate output filename
        output_filename = file_handler.generate_output_filename(
            sanitize_filename(file.filename),
            output_format
        )
        output_file_path = file_handler.get_temp_path(f"{uuid.uuid4()}_{output_filename}")
        
        # Perform conversion
        await cloudconvert_service.convert_image(
            input_file_path,
            output_format,
            output_file_path
        )
        
        # Generate download URL
        download_url = f"/api/download/{output_file_path.name}"
        
        return {
            "success": True,
            "message": "Conversion completed successfully",
            "original_filename": file.filename,
            "output_filename": output_filename,
            "download_url": download_url,
            "input_format": input_format,
            "output_format": output_format
        }
        
    except ConversionError as e:
        # Clean up files
        if input_file_path:
            file_handler.delete_file(input_file_path)
        if output_file_path:
            file_handler.delete_file(output_file_path)
        
        raise HTTPException(status_code=500, detail=str(e))
        
    except HTTPException:
        # Re-raise HTTP exceptions
        if input_file_path:
            file_handler.delete_file(input_file_path)
        raise
        
    except Exception as e:
        # Clean up files
        if input_file_path:
            file_handler.delete_file(input_file_path)
        if output_file_path:
            file_handler.delete_file(output_file_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )
    finally:
        # Always clean up input file
        if input_file_path and input_file_path.exists():
            file_handler.delete_file(input_file_path)


@router.get("/api/download/{filename}")
async def download_file(filename: str):
    """
    Download a converted file.
    
    Args:
        filename: Name of the file to download
        
    Returns:
        The file as a download response
    """
    # Sanitize filename to prevent directory traversal
    filename = sanitize_filename(filename)
    file_path = file_handler.get_temp_path(filename)
    
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found. It may have been deleted or expired."
        )
    
    # Extract the user-friendly filename (remove UUID prefix)
    if '_' in filename:
        display_filename = '_'.join(filename.split('_')[1:])
    else:
        display_filename = filename
    
    return FileResponse(
        path=file_path,
        filename=display_filename,
        media_type="application/octet-stream",
        background=None  # We'll handle cleanup separately
    )

