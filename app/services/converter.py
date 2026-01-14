"""
CloudConvert API integration service.
Handles image format conversion using the CloudConvert API.
"""

import httpx
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any
from fastapi import HTTPException
from app.config import settings


class ConversionError(Exception):
    """Custom exception for conversion errors."""
    pass


class CloudConvertService:
    """Service for interacting with CloudConvert API."""
    
    def __init__(self):
        self.api_key = settings.cloudconvert_api_key
        self.api_url = settings.cloudconvert_api_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def convert_image(
        self,
        input_file_path: Path,
        output_format: str,
        output_file_path: Path,
        quality: Optional[int] = None,
        resize_width: Optional[int] = None,
        resize_height: Optional[int] = None
    ) -> Path:
        """
        Convert an image file to a different format.
        
        Args:
            input_file_path: Path to input file
            output_format: Desired output format (jpeg, png, webp, gif)
            output_file_path: Path where converted file should be saved
            quality: Optional quality for lossy formats (1-100)
            resize_width: Optional target width in pixels
            resize_height: Optional target height in pixels
            
        Returns:
            Path to the converted file
            
        Raises:
            ConversionError: If conversion fails
        """
        if not self.api_key or self.api_key == "your_api_key_here":
            raise ConversionError(
                "CloudConvert API key not configured. "
                "Please set CLOUDCONVERT_API_KEY in your .env file."
            )
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                # Step 1: Create a job
                job_response = await self._create_job(
                    client,
                    output_format,
                    quality=quality,
                    resize_width=resize_width,
                    resize_height=resize_height
                )
                
                # Step 2: Upload the file
                upload_task = self._find_task(job_response, "import/upload")
                await self._upload_file(client, upload_task, input_file_path)
                
                # Step 3: Wait for conversion to complete
                job_id = job_response["data"]["id"]
                completed_job = await self._wait_for_job(client, job_id)
                
                # Step 4: Download the converted file
                export_task = self._find_task(completed_job, "export/url")
                await self._download_file(client, export_task, output_file_path)
                
                return output_file_path
                
        except httpx.HTTPError as e:
            raise ConversionError(f"Network error during conversion: {str(e)}")
        except Exception as e:
            raise ConversionError(f"Conversion failed: {str(e)}")
    
    async def _create_job(
        self,
        client: httpx.AsyncClient,
        output_format: str,
        quality: Optional[int] = None,
        resize_width: Optional[int] = None,
        resize_height: Optional[int] = None
    ) -> Dict[str, Any]:
        """Create a conversion job."""
        # Normalize format
        if output_format == 'jpg':
            output_format = 'jpeg'
        
        convert_task: Dict[str, Any] = {
            "operation": "convert",
            "input": "import-my-file",
            "output_format": output_format
        }
        
        if quality is not None:
            convert_task["quality"] = quality
        if resize_width is not None:
            convert_task["width"] = resize_width
        if resize_height is not None:
            convert_task["height"] = resize_height
        
        job_data = {
            "tasks": {
                "import-my-file": {
                    "operation": "import/upload"
                },
                "convert-my-file": {
                    **convert_task
                },
                "export-my-file": {
                    "operation": "export/url",
                    "input": "convert-my-file"
                }
            }
        }
        
        response = await client.post(
            f"{self.api_url}/jobs",
            json=job_data,
            headers=self.headers
        )
        
        if response.status_code not in [200, 201]:
            error_detail = response.json().get("message", "Unknown error")
            raise ConversionError(f"Failed to create job: {error_detail}")
        
        return response.json()
    
    def _find_task(self, job_data: Dict[str, Any], operation: str) -> Dict[str, Any]:
        """Find a specific task in the job data."""
        tasks = job_data["data"]["tasks"]
        for task in tasks:
            if task["operation"] == operation:
                return task
        raise ConversionError(f"Task with operation '{operation}' not found")
    
    async def _upload_file(
        self,
        client: httpx.AsyncClient,
        upload_task: Dict[str, Any],
        file_path: Path
    ) -> None:
        """Upload file to CloudConvert."""
        upload_url = upload_task["result"]["form"]["url"]
        upload_params = upload_task["result"]["form"]["parameters"]
        
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.name, f, 'application/octet-stream')}
            response = await client.post(
                upload_url,
                data=upload_params,
                files=files
            )
        
        if response.status_code not in [200, 201]:
            raise ConversionError(f"File upload failed: {response.text}")
    
    async def _wait_for_job(
        self,
        client: httpx.AsyncClient,
        job_id: str,
        max_wait: int = 120
    ) -> Dict[str, Any]:
        """Wait for job to complete."""
        waited = 0
        while waited < max_wait:
            response = await client.get(
                f"{self.api_url}/jobs/{job_id}",
                headers=self.headers
            )
            
            if response.status_code != 200:
                raise ConversionError(f"Failed to check job status: {response.text}")
            
            job_data = response.json()
            status = job_data["data"]["status"]
            
            if status == "finished":
                return job_data
            elif status == "error":
                error_msg = job_data["data"].get("message", "Unknown error")
                raise ConversionError(f"Conversion failed: {error_msg}")
            
            # Wait before checking again
            await asyncio.sleep(2)
            waited += 2
        
        raise ConversionError("Conversion timed out")
    
    async def _download_file(
        self,
        client: httpx.AsyncClient,
        export_task: Dict[str, Any],
        output_path: Path
    ) -> None:
        """Download the converted file."""
        download_url = export_task["result"]["files"][0]["url"]
        
        response = await client.get(download_url)
        
        if response.status_code != 200:
            raise ConversionError(f"Failed to download converted file: {response.text}")
        
        with open(output_path, 'wb') as f:
            f.write(response.content)


# Create singleton instance
cloudconvert_service = CloudConvertService()
