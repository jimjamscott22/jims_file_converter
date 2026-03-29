# AGENTS.md

This repository is a small FastAPI + vanilla HTML/CSS/JS app for file conversion.

## Project Shape

- Backend entry point: `app/main.py`
- API routes: `app/api/routes.py`
- Main page template: `templates/index.html`
- Frontend behavior: `static/js/app.js`
- Frontend styling: `static/css/style.css`
- Local startup script: `run.py`

## Working Rules

- Keep the app lightweight. Prefer simple HTML, CSS, and vanilla JavaScript over adding frameworks or build tooling.
- Preserve the current interaction model unless the task explicitly calls for UX changes.
- Make backend changes in a way that keeps the local dev flow straightforward: `uv run python run.py`.
- Avoid unnecessary dependencies for small UI or API changes.

## UI Style Direction

- Preserve the current visual direction: cool hacker-aesthetic, but not neon green and not retro terminal parody.
- Prefer dark glassy surfaces, steel/slate backgrounds, indigo or icy-cyan accents, and restrained glow.
- Do not switch the UI back to bright generic SaaS cards or warm gradient branding.
- Avoid green body text, Matrix-style effects, or overly aggressive cyberpunk styling.
- Keep the design clean and usable first; the “hacker” feel should come from tone, contrast, texture, and hierarchy.
- Use subtle grid, scanline, or console-inspired details only when they stay low-noise.
- Maintain strong readability on desktop and mobile.

## Frontend Notes

- Treat the main converter as the primary workspace.
- Keep copy concise and utility-focused.
- If adjusting the UI, prefer editing `templates/index.html` and `static/css/style.css` without changing JS behavior unless needed.
- Motion should stay restrained: small hover shifts, fade-ups, and subtle emphasis are preferred over flashy animation.

## When Updating This File

- Update this document when the project structure changes materially or when the visual direction changes on purpose.
