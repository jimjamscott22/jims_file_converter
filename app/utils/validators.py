"""
File validation utilities.
Validates file types, sizes, and formats before processing.
"""

import os
import magic
from pathlib import Path
from typing import Tuple, Optional
from fastapi import UploadFile, HTTPException
from app.config import settings


def get_file_extension(filename: str) -> str:
    """Extract file extension from filename."""
    return Path(filename).suffix.lower().lstrip('.')


def validate_file_size(file: UploadFile) -> None:
    """
    Validate that file size is within allowed limits.
    
    Args:
        file: The uploaded file
        
    Raises:
        HTTPException: If file is too large
    """
    # Check file size by reading it
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > settings.max_file_size_bytes:
        max_mb = settings.max_file_size_mb
        actual_mb = round(file_size / (1024 * 1024), 2)
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {max_mb}MB, got {actual_mb}MB"
        )


def validate_file_format(filename: str, file_content: Optional[bytes] = None) -> str:
    """
    Validate that file format is supported.
    
    Args:
        filename: The name of the file
        file_content: Optional file content for MIME type detection
        
    Returns:
        The validated file extension
        
    Raises:
        HTTPException: If file format is not supported
    """
    extension = get_file_extension(filename)
    
    if extension not in settings.supported_formats:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format: .{extension}. "
                   f"Supported formats: {', '.join(settings.supported_formats)}"
        )
    
    # Additional MIME type validation if content is provided
    if file_content:
        try:
            mime = magic.from_buffer(file_content, mime=True)
            # Check if MIME type matches expected image types
            if not mime.startswith('image/'):
                raise HTTPException(
                    status_code=400,
                    detail=f"File is not a valid image. Detected type: {mime}"
                )
        except Exception as e:
            # If magic fails, we'll rely on extension validation
            print(f"MIME type detection failed: {e}")
    
    return extension


def validate_output_format(output_format: str) -> str:
    """
    Validate that output format is supported.
    
    Args:
        output_format: The requested output format
        
    Returns:
        The validated output format
        
    Raises:
        HTTPException: If output format is not supported
    """
    output_format = output_format.lower().strip()
    
    if output_format not in settings.supported_formats:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported output format: {output_format}. "
                   f"Supported formats: {', '.join(settings.supported_formats)}"
        )
    
    return output_format


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent directory traversal and other issues.
    
    Args:
        filename: The original filename
        
    Returns:
        Sanitized filename
    """
    # Get just the filename without path
    filename = os.path.basename(filename)
    
    # Remove any potentially dangerous characters
    dangerous_chars = ['/', '\\', '..', '<', '>', ':', '"', '|', '?', '*']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    
    # Limit filename length
    name, ext = os.path.splitext(filename)
    if len(name) > 100:
        name = name[:100]
    
    return name + ext

