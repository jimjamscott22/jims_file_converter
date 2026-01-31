# Future Enhancements for Jim's File Converter

## High Priority

### Testing
- No tests exist in the project. pytest and pytest-asyncio are in requirements-dev.txt but commented out.
- Unit tests needed for: validators, file handler, local converter, CloudConvert service.
- Integration tests needed for all API endpoints.
- The local Pillow converter is especially easy to test since it has no external dependencies.

### Rate Limiting
- No auth or rate limiting exists. Anyone with the URL can consume CloudConvert API quota.
- Add IP-based rate limiting using `slowapi` (FastAPI-compatible).
- Consider a simple API key or token system for production use.

### CORS Lockdown
- CORS currently allows all origins (`*`) in app/main.py.
- Restrict to the actual frontend origin for production deployments.

## Medium Priority

### Batch Conversion
- Currently only single-file conversion is supported.
- Allow users to drop multiple files and convert them all at once.
- Provide a zip download for batch results.
- Show per-file progress in the UI.

### More File Formats
- PDF conversion (image-to-PDF, PDF-to-image) is a common need.
- SVG support (raster-to-SVG, SVG-to-raster).
- TIFF, BMP, ICO, AVIF -- CloudConvert supports these already; mostly requires updating the allowed formats in app/utils/validators.py and app/config.py.
- Pillow can handle TIFF, BMP, and ICO locally as well.

### Docker Support
- No Dockerfile or docker-compose.yml exists.
- Containerizing the app would simplify deployment and sharing.

### Dark Mode
- The CSS (static/css/style.css, 805 lines) has no theme support.
- Implement a CSS custom properties-based dark/light toggle.

### Image Metadata Options
- Option to strip EXIF data (privacy feature).
- Option to preserve EXIF data during conversion.
- Display file metadata (dimensions, file size, color space) in the UI.

## Low Priority

### WebSocket Progress
- Replace the current polling-based progress animation with real-time WebSocket updates.
- FastAPI supports WebSockets natively.
- Mostly useful for CloudConvert conversions (local ones are near-instant).

### Conversion History
- In-memory or localStorage-based list of recent conversions.
- Re-download links while files still exist in temp/.

### CI/CD Pipeline
- No GitHub Actions or similar automation.
- A basic workflow to run linting and tests on push would catch regressions.

### Clipboard Paste Support
- Support pasting images from clipboard (Ctrl+V) in the drop zone.
- Support dropping URLs to remote images (fetch and convert).

### Before/After Preview
- Show a side-by-side preview so users can see quality impact before downloading.
- Especially useful with the quality slider for JPEG/WebP.

### Compression Target Mode
- Beyond the quality slider, add an "optimize for file size" mode.
- Let users target a specific output size (e.g., "under 500KB").

### Accessibility
- Add ARIA labels throughout the UI.
- Keyboard navigation for the drop zone.
- Screen reader support.

## Completed

- [x] Local Pillow fallback (2026-01-31) -- Image conversions now run locally via Pillow. CloudConvert is only used as a fallback if Pillow fails.
