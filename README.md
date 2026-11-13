# BITBYTE

BITBYTE is a food search and meal discovery app with a fixed AI food assistant. It combines USDA FoodData Central nutrition search, recipe search, and a local Ollama model.

## Stack

- **Frontend:** React, TypeScript, Vite, CSS
- **Backend:** Node.js, Express, TypeScript
- **AI for all features:** Ollama `qwen2.5vl:7b` (text summaries, chat, meal plans, and image analysis)
- **Food data:** USDA FoodData Central and TheMealDB

## Features

- Search food and nutrition records, with a generated overview and paginated results.
- Search recipes alongside the first page of food results.
- Keep a food assistant and contextual suggestion fixed on screen across home and search pages.
- Ask food questions, request meal routines, and analyze a meal photo for estimated foods and nutrients.
- Save food and recipe results, store food preferences, and generate a meal plan in the profile panel.
- Persist profile details, saved items, meal plan, and recent chat in the current browser.

The profile is browser-local and has no account sign-in or cross-device sync. Photo nutrition is an estimate: a picture cannot reliably show exact ingredients, preparation, or portion weight.

## Requirements

- Node.js LTS and npm
- Ollama with `qwen2.5vl:7b` installed
- Optional USDA FoodData Central API key for higher-volume food search

Pull and start the model:

```bash
ollama pull qwen2.5vl:7b
ollama serve
```

Ollama must be reachable from the backend. The default address is `http://localhost:11434`.

## Setup

Install frontend and backend dependencies:

```bash
cd backend && npm install
cd ../frontend && npm install
```

Create `backend/.env`:

```env
PORT=5000
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5vl:7b
USDA_API_KEY=your_usda_api_key
# Set this if the frontend is served from a different origin:
FRONTEND_ORIGIN=http://localhost:5173
```

Create `frontend/.env.local`:

```env
VITE_API_URL=http://localhost:5000
```

Run the backend and frontend in separate terminals:

```bash
cd backend && npm run dev
```

```bash
cd frontend && npm run dev
```

The Vite output shows the frontend URL. The backend listens on port 5000 by default.

## API routes

- `GET /api/search?query=<food>&page=1&pageSize=50` — search foods, fetch matching recipes on the first page, and generate a grounded summary.
- `POST /api/search/chat` — food assistant chat.
- `POST /api/search/plan` — generate a meal plan from a goal and preferences.
- `POST /api/search/image` — analyze a base64 JPEG, PNG, or WebP meal image with Qwen2.5-VL.

Food search requests 50 results per page and follows the USDA pagination metadata as the user loads more. The USDA service and model still apply their own availability and rate limits. The app falls back to its local food samples only when `VITE_API_URL` is not configured.

## Credentials and privacy

Keep API keys in backend environment variables. Do not commit `.env` files or put private credentials in `VITE_` variables, which are exposed to browser code. Uploaded images are sent to the configured Ollama model and are not saved by the BITBYTE backend. User profile data and recent conversation are stored in browser local storage.
