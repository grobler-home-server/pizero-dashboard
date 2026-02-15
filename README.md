# Pizero Dashboard

This directory contains the server-side components for the Pizero Dashboard.

## Components
- **Dashboard Server**: A Python HTTP server (`server.py`) independent of Home Assistant that serves the dashboard image.
- **Renderer**: A Python script (`renderer.py`) that fetches data from Home Assistant and generates a 1080p PNG image.

## Service
The dashboard is managed by a systemd service: `pizero-dashboard.service`.
- **Status**: `systemctl status pizero-dashboard`
- **Port**: 8085
- **Endpoint**: `http://localhost:8085/render` (Triggers a fresh render)

## Integration
Home Assistant triggers a render via a shell command when specific sensors change. The Pizero then fetches the generated image from this server.
