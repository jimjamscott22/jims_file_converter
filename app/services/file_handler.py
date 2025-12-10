"""
File handling service.
Manages file uploads, downloads, and temporary storage.
"""

import os
import uuid
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
from fastapi import UploadFile
from app.config import settings


class FileHandler:
    """Handles file operations for uploads and downloads."""
    
    def __init__(self):
        self.temp_dir = settings.temp_dir
        
    async def save_upload(self, file: UploadFile) -> Path:
        """
        Save an uploaded file to temporary storage.
        
        Args:
            file: The uploaded file
            
        Returns:
            Path to the saved file
        """
        # Generate unique filename to avoid collisions
        file_id = str(uuid.uuid4())
        original_name = file.filename or "upload"
        extension = Path(original_name).suffix
        
        filename = f"{file_id}{extension}"
        file_path = self.temp_dir / filename
        
        # Save file
        content = await file.read()
        with open(file_path, 'wb') as f:
            f.write(content)
        
        return file_path
    
    def get_temp_path(self, filename: str) -> Path:
        """
        Get path for a temporary file.
        
        Args:
            filename: The filename
            
        Returns:
            Full path to the file
        """
        return self.temp_dir / filename
    
    def delete_file(self, file_path: Path) -> None:
        """
        Delete a file from temporary storage.
        
        Args:
            file_path: Path to the file to delete
        """
        try:
            if file_path.exists():
                file_path.unlink()
                print(f"Deleted temporary file: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
    
    async def cleanup_old_files(self, max_age_hours: int = 1) -> None:
        """
        Clean up temporary files older than specified age.
        
        Args:
            max_age_hours: Maximum age of files to keep in hours
        """
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        for file_path in self.temp_dir.glob('*'):
            if file_path.is_file():
                # Get file modification time
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                
                if file_time < cutoff_time:
                    self.delete_file(file_path)
    
    def generate_output_filename(self, original_filename: str, output_format: str) -> str:
        """
        Generate output filename with new extension.
        
        Args:
            original_filename: Original file name
            output_format: New format extension
            
        Returns:
            New filename with updated extension
        """
        name = Path(original_filename).stem
        # Normalize format (jpg -> jpeg for consistency)
        if output_format == 'jpg':
            output_format = 'jpeg'
        
        return f"{name}_converted.{output_format}"


# Create singleton instance
file_handler = FileHandler()

