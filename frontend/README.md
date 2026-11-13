# BITBYTE frontend

React + TypeScript + Vite interface for BITBYTE. It includes food search, Qwen-powered summaries and chat, locally saved profile data, meal planning, and meal photo upload.

For full setup, backend configuration, and Ollama instructions, see the [project README](../README.md).

Set `VITE_API_URL=http://localhost:5000` in `.env.local` to connect the frontend to the API. Without it, the search UI uses the local sample dataset; AI features still expect the backend at `http://localhost:5000`.
