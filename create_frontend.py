import os, zipfile, textwrap
root = os.path.expanduser("~/BITBYTE/frontend")
files={
"package.json": r'''{
  "name": "bitbyte-frontend",
  "private": true,
  "version": "0.0.1",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@tanstack/react-query": "^5.90.0",
    "axios": "^1.12.0",
    "framer-motion": "^12.23.0",
    "lucide-react": "^0.468.0",
    "react": "^19.1.0",
    "react-dom": "^19.1.0",
    "react-router-dom": "^7.9.0",
    "recharts": "^2.15.4"
  },
  "devDependencies": {
    "@tailwindcss/vite": "^4.1.13",
    "@types/react": "^19.1.10",
    "@types/react-dom": "^19.1.7",
    "@vitejs/plugin-react": "^5.0.4",
    "tailwindcss": "^4.1.13",
    "typescript": "~5.9.2",
    "vite": "^7.1.7"
  }
}''',
"index.html": r'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#171321" />
    <meta name="description" content="BITBYTE — explore food, nutrition, recipes and ingredients." />
    <title>BITBYTE — The Food Universe</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>''',
"vite.config.ts": r'''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
})''',
"tsconfig.json": r'''{
  "files": [],
  "references": [
    { "path": "./tsconfig.app.json" },
    { "path": "./tsconfig.node.json" }
  ]
}''',
"tsconfig.app.json": r'''{
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.app.tsbuildinfo",
    "target": "ES2022",
    "useDefineForClassFields": true,
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "verbatimModuleSyntax": true,
    "moduleDetection": "force",
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"]
}''',
"tsconfig.node.json": r'''{
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.node.tsbuildinfo",
    "target": "ES2023",
    "lib": ["ES2023"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "verbatimModuleSyntax": true,
    "moduleDetection": "force",
    "noEmit": true,
    "strict": true
  },
  "include": ["vite.config.ts"]
}''',
".gitignore": r'''node_modules
dist
.env
.env.local
*.tsbuildinfo
''',
"src/main.tsx": r'''import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './styles.css'

createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)''',
"src/types.ts": r'''export type FoodCategory = 'Nutrition' | 'Recipes' | 'Protein' | 'Ingredients' | 'Food science'

export interface FoodResult {
  id: string
  title: string
  category: FoodCategory
  description: string
  image: string
  tags: string[]
  calories?: number
  protein?: number
}

export interface SearchResponse {
  query: string
  total: number
  results: FoodResult[]
}''',
"src/data/food.ts": r'''import type { FoodResult } from '../types'

export const foodData: FoodResult[] = [
  {
    id: 'chicken',
    title: 'Chicken breast',
    category: 'Nutrition',
    description: 'A lean, protein-rich staple. Values vary depending on whether it is raw or cooked.',
    image: 'https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=900&q=85',
    tags: ['chicken', 'protein', 'lean meat', 'nutrition', 'meal prep'],
    calories: 165,
    protein: 31,
  },
  {
    id: 'paneer',
    title: 'Paneer',
    category: 'Nutrition',
    description: 'A versatile fresh cheese used in Indian cooking, with protein and calcium.',
    image: 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=900&q=85',
    tags: ['paneer', 'vegetarian', 'protein', 'indian', 'cheese'],
    calories: 265,
    protein: 18,
  },
  {
    id: 'overnight-oats',
    title: 'Overnight oats',
    category: 'Recipes',
    description: 'A make-ahead breakfast made with oats, milk or yogurt, and your favorite toppings.',
    image: 'https://images.unsplash.com/photo-1517673132405-a56a62b18caf?auto=format&fit=crop&w=900&q=85',
    tags: ['oats', 'breakfast', 'recipe', 'fiber', 'milk'],
  },
  {
    id: 'lentils',
    title: 'Lentils',
    category: 'Protein',
    description: 'An affordable plant-based source of protein, fiber and minerals.',
    image: 'https://images.unsplash.com/photo-1515543904379-3d757ef7f2f5?auto=format&fit=crop&w=900&q=85',
    tags: ['lentils', 'dal', 'protein', 'vegetarian', 'plant based'],
    calories: 116,
    protein: 9,
  },
  {
    id: 'avocado',
    title: 'Avocado',
    category: 'Ingredients',
    description: 'Creamy fruit rich in unsaturated fats and commonly used in salads and toast.',
    image: 'https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?auto=format&fit=crop&w=900&q=85',
    tags: ['avocado', 'healthy fats', 'ingredient', 'salad'],
  },
  {
    id: 'fermentation',
    title: 'How fermentation works',
    category: 'Food science',
    description: 'Microorganisms transform food, changing its flavor, texture and sometimes shelf life.',
    image: 'https://images.unsplash.com/photo-157 (placeholder)',
    tags: ['fermentation', 'food science', 'microbes', 'kimchi', 'yogurt'],
  },
]

export function searchFood(query: string): FoodResult[] {
  const normalized = query.trim().toLowerCase()
  if (!normalized) return []

  const terms = normalized.split(/\s+/).filter(Boolean)
  return foodData
    .map((item) => {
      const searchable = `${item.title} ${item.description} ${item.category} ${item.tags.join(' ')}`.toLowerCase()
      const score = terms.reduce((total, term) => {
        if (item.title.toLowerCase() === term) return total + 10
        if (item.title.toLowerCase().includes(term)) return total + 5
        if (item.tags.some((tag) => tag.includes(term))) return total + 3
        if (searchable.includes(term)) return total + 1
        return total
      }, 0)
      return { item, score }
    })
    .filter(({ score }) => score > 0)
    .sort((a, b) => b.score - a.score)
    .map(({ item }) => item)
}''',
"src/services/search.ts": r'''import axios from 'axios'
import type { SearchResponse } from '../types'
import { searchFood } from '../data/food'

const API_BASE_URL = import.meta.env.VITE_API_URL

export async function searchFoods(query: string): Promise<SearchResponse> {
  // If the backend URL is configured, use the real API.
  if (API_BASE_URL) {
    const response = await axios.get<SearchResponse>(`${API_BASE_URL}/api/search`, {
      params: { q: query },
    })
    return response.data
  }

  // Frontend-only fallback keeps search interactive before backend work begins.
  const results = searchFood(query)
  return { query, total: results.length, results }
}''',
"src/components/SearchBar.tsx": r'''import { ArrowUp, Search, X } from 'lucide-react'
import { FormEvent, useState } from 'react'

interface SearchBarProps {
  initialValue?: string
  onSearch: (query: string) => void
  compact?: boolean
}

export default function SearchBar({ initialValue = '', onSearch, compact = false }: SearchBarProps) {
  const [query, setQuery] = useState(initialValue)

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const trimmed = query.trim()
    if (trimmed) onSearch(trimmed)
  }

  return (
    <form className={`search-box ${compact ? 'search-box--compact' : ''}`} onSubmit={submit}>
      <Search size={20} className="search-box__icon" aria-hidden="true" />
      <input
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        placeholder="What are you craving today?"
        aria-label="Search food"
      />
      {query && (
        <button className="icon-button clear-button" type="button" onClick={() => setQuery('')} aria-label="Clear search">
          <X size={17} />
        </button>
      )}
      <button className="search-submit" type="submit" aria-label="Search">
        <ArrowUp size={20} />
      </button>
    </form>
  )
}''',
"src/components/FoodCard.tsx": r'''import { ArrowUpRight, Flame, Tags } from 'lucide-react'
import type { FoodResult } from '../types'

export default function FoodCard({ item }: { item: FoodResult }) {
  return (
    <article className="food-card">
      <div className="food-card__image-wrap">
        <img src={item.image} alt="" className="food-card__image" loading="lazy" />
        <span className="food-card__category">{item.category}</span>
        <button className="food-card__open" aria-label={`Open ${item.title}`}>
          <ArrowUpRight size={18} />
        </button>
      </div>
      <div className="food-card__body">
        <h3>{item.title}</h3>
        <p>{item.description}</p>
        {(item.calories !== undefined || item.protein !== undefined) && (
          <div className="food-card__facts">
            {item.calories !== undefined && <span><Flame size={14} /> {item.calories} kcal</span>}
            {item.protein !== undefined && <span><Tags size={14} /> {item.protein}g protein</span>}
          </div>
        )}
      </div>
    </article>
  )
}''',
"src/App.tsx": r'''import { ArrowDownRight, ArrowRight, Sparkles, Utensils, X } from 'lucide-react'
import { useState } from 'react'
import SearchBar from './components/SearchBar'
import FoodCard from './components/FoodCard'
import { foodData } from './data/food'
import { searchFoods } from './services/search'
import type { FoodResult } from './types'

const categories = [
  { label: '🥑 Nutrition', query: 'nutrition' },
  { label: '🍜 Recipes', query: 'recipe' },
  { label: '🥩 Protein', query: 'protein' },
  { label: '🍓 Ingredients', query: 'ingredient' },
  { label: '🍕 Food science', query: 'food science' },
]

export default function App() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<FoodResult[]>([])
  const [searched, setSearched] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function runSearch(value: string) {
    setQuery(value)
    setSearched(true)
    setLoading(true)
    setError('')
    try {
      const response = await searchFoods(value)
      setResults(response.results)
    } catch {
      setError('Search could not be completed. Check the backend connection and try again.')
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  function resetSearch() {
    setQuery('')
    setResults([])
    setSearched(false)
    setError('')
  }

  return (
    <main className="site-shell">
      <div className="ambient ambient--one" />
      <div className="ambient ambient--two" />

      <header className="navbar">
        <a className="brand" href="/" onClick={(event) => { event.preventDefault(); resetSearch() }}>
          <span className="brand-mark"><Utensils size={19} strokeWidth={2.7} /></span>
          <span>BITBYTE<span className="brand-dot">.</span></span>
        </a>
        <nav className="nav-links" aria-label="Main navigation">
          <a href="#discover">Discover</a>
          <a href="#recipes" onClick={() => runSearch('recipe')}>Recipes</a>
        </nav>
        <button className="nav-avatar" aria-label="User profile">B</button>
      </header>

      {!searched ? (
        <section className="hero">
          <div className="hero-kicker"><span className="kicker-dot" /> THE FOOD UNIVERSE <span className="kicker-line" /></div>
          <h1>FOOD IS MORE<br /><span>THAN JUST FOOD.</span></h1>
          <div className="hero-subline">
            <p>Explore. Eat. Understand.</p>
            <span>Your curiosity deserves a better search engine.</span>
          </div>

          <div className="hero-art">
            <div className="art-sticker sticker--tomato">TASTE<br />THE<br />WORLD</div>
            <div className="art-sticker sticker--star"><Sparkles size={27} /> GOOD<br />FOOD<br />ENERGY</div>
            <div className="food-photo photo--main">
              <img src="https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1200&q=90" alt="Colourful food spread" />
              <span className="photo-label">A LITTLE BIT OF EVERYTHING</span>
            </div>
            <div className="food-photo photo--small">
              <img src="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=700&q=85" alt="Fresh salad bowl" />
            </div>
            <div className="art-note"><span>01 / 05</span><span>DISCOVER SOMETHING DELICIOUS <ArrowDownRight size={14} /></span></div>
          </div>

          <div className="home-search">
            <SearchBar onSearch={runSearch} />
            <div className="search-hint"><span>TRY SEARCHING</span><span>anything edible, really ↗</span></div>
          </div>

          <div className="category-pills">
            {categories.map((category) => (
              <button key={category.label} onClick={() => runSearch(category.query)}>{category.label}</button>
            ))}
          </div>
        </section>
      ) : (
        <section className="results-page">
          <div className="results-top">
            <a className="brand brand--small" href="/" onClick={(event) => { event.preventDefault(); resetSearch() }}>
              <span className="brand-mark"><Utensils size={17} /></span><span>BITBYTE<span className="brand-dot">.</span></span>
            </a>
            <SearchBar initialValue={query} compact onSearch={runSearch} />
            <button className="icon-button result-close" onClick={resetSearch} aria-label="Back to home"><X size={19} /></button>
          </div>
          <div className="result-tabs">
            <span className="tab-active">All results</span><button onClick={() => runSearch(`${query} nutrition`)}>Nutrition</button><button onClick={() => runSearch(`${query} recipe`)}>Recipes</button><button onClick={() => runSearch(`${query} protein`)}>Protein</button>
          </div>
          <div className="results-content">
            <div className="results-heading">
              <div><span className="eyebrow">SEARCHING THE FOOD UNIVERSE</span><h2>Results for <em>“{query}”</em></h2></div>
              <button className="text-button" onClick={resetSearch}>New search <ArrowRight size={15} /></button>
            </div>
            <div className="ai-summary">
              <div className="ai-summary__top"><span><Sparkles size={15} /> BITBYTE INTELLIGENCE</span><span className="demo-tag">PREVIEW</span></div>
              <h3>Good things start with curiosity.</h3>
              <p>This is the first search experience. Results are currently powered by a small local food dataset. Next, we’ll connect real nutrition and recipe sources, then add grounded AI summaries.</p>
            </div>
            {error && <p className="error-message">{error}</p>}
            {loading ? <div className="loading-state"><span className="loader" /> Searching the food universe…</div> : (
              results.length ? (
                <div className="result-grid">{results.map((item) => <FoodCard key={item.id} item={item} />)}</div>
              ) : (
                <div className="empty-state"><span>¯\\_(ツ)_/¯</span><h3>No food found. Yet.</h3><p>Try “paneer”, “protein”, “oats” or “food science”.</p></div>
              )
            )}
          </div>
        </section>
      )}

      <section className="manifesto" id="discover">
        <div className="manifesto__left"><span className="eyebrow">BITBYTE INTELLIGENCE <Sparkles size={14} /></span><h2>EAT<br /><em>SMARTER.</em></h2></div>
        <div className="manifesto__right"><p>Not another recipe website.<br /><strong>A whole new way to explore food.</strong></p><span className="manifesto-arrow"><ArrowRight size={25} /></span></div>
      </section>

      {!searched && (
        <section className="explore-section" id="recipes">
          <div className="section-head"><div><span className="eyebrow">A WORLD ON YOUR PLATE</span><h2>Explore the delicious <em>chaos.</em></h2></div><span className="section-index">01 — 04</span></div>
          <div className="explore-grid">
            {foodData.slice(0, 4).map((item, index) => (
              <button className={`explore-tile explore-tile--${index + 1}`} key={item.id} onClick={() => runSearch(item.title)}>
                <img src={item.image} alt="" loading="lazy" />
                <span className="tile-number">0{index + 1}</span>
                <span className="tile-title">{['Food discovery', 'Nutrition explorer', 'Recipe universe', 'Ingredient library'][index]}</span>
                <span className="tile-arrow"><ArrowRight size={17} /></span>
              </button>
            ))}
          </div>
        </section>
      )}

      <footer className="footer"><a className="brand brand--small" href="#" onClick={(event) => { event.preventDefault(); resetSearch() }}>BITBYTE<span className="brand-dot">.</span></a><span>MADE FOR THE CURIOUS & HUNGRY.</span><span>© BITBYTE 2026</span></footer>
    </main>
  )
}''',
"src/styles.css": r'''@import "tailwindcss";

:root {
  font-family: "DM Sans", sans-serif;
  color: #fff;
  background: #171321;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  --bg: #171321;
  --lime: #d9ff45;
  --coral: #ff674d;
  --lavender: #a88bff;
  --muted: #aaa2b7;
  --panel: #241d31;
  --line: rgba(255,255,255,.13);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin: 0; min-width: 320px; background: var(--bg); overflow-x: hidden; }
button, input { font: inherit; }
button { cursor: pointer; }
a { color: inherit; text-decoration: none; }
.site-shell { min-height: 100vh; position: relative; overflow: hidden; }
.ambient { position: absolute; pointer-events: none; border-radius: 50%; filter: blur(100px); opacity: .16; }
.ambient--one { width: 380px; height: 380px; background: var(--lavender); top: 180px; left: -220px; }
.ambient--two { width: 300px; height: 300px; background: var(--coral); top: 650px; right: -200px; }
.navbar { width: min(1180px, calc(100% - 48px)); margin: 0 auto; height: 84px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--line); position: relative; z-index: 2; }
.brand { display: inline-flex; align-items: center; gap: 10px; font-family: "Space Grotesk", sans-serif; font-size: 21px; font-weight: 700; letter-spacing: -.8px; }
.brand-mark { display: grid; place-items: center; width: 36px; height: 36px; color: var(--bg); background: var(--lime); border-radius: 11px; }
.brand-dot { color: var(--lime); }
.nav-links { display: flex; gap: 34px; color: #d0cbd7; font-size: 13px; }
.nav-links a:hover { color: var(--lime); }
.nav-avatar { width: 34px; height: 34px; border: 1px solid var(--line); border-radius: 50%; background: #332a43; color: var(--lime); font-weight: 700; }
.hero { width: min(1040px, calc(100% - 40px)); margin: 0 auto; padding: 65px 0 72px; position: relative; }
.hero-kicker, .eyebrow { display: flex; align-items: center; gap: 9px; color: var(--lime); font-size: 10px; font-weight: 700; letter-spacing: 1.8px; }
.kicker-dot { width: 7px; height: 7px; background: var(--lime); border-radius: 50%; box-shadow: 0 0 12px #d9ff4570; }
.kicker-line { width: 42px; height: 1px; background: #71677e; margin-left: 4px; }
.hero h1 { font-family: "Space Grotesk", sans-serif; font-size: clamp(48px, 8vw, 92px); line-height: .93; letter-spacing: -5px; font-weight: 700; margin: 25px 0 18px; }
.hero h1 span { color: var(--lime); }
.hero-subline { display: flex; align-items: center; gap: 18px; flex-wrap: wrap; }
.hero-subline p { margin: 0; font-size: 18px; font-weight: 600; }
.hero-subline span { color: var(--muted); font-size: 13px; }
.hero-art { height: 330px; margin: 34px 0 22px; position: relative; }
.food-photo { overflow: hidden; position: absolute; border: 5px solid var(--bg); box-shadow: 0 18px 50px #0003; }
.food-photo img { width: 100%; height: 100%; object-fit: cover; display: block; }
.photo--main { width: 58%; height: 285px; left: 16%; top: 10px; border-radius: 5px 42px 5px 5px; transform: rotate(-2deg); }
.photo--small { width: 26%; height: 170px; right: 9%; bottom: 3px; border-radius: 50% 5px 5px 5px; transform: rotate(5deg); }
.photo-label { position: absolute; left: 14px; bottom: 13px; background: var(--lime); color: var(--bg); padding: 7px 10px; font-size: 9px; font-weight: 800; letter-spacing: 1px; }
.art-sticker { position: absolute; z-index: 2; font-family: "Space Grotesk", sans-serif; font-weight: 700; text-align: center; line-height: 1; }
.sticker--tomato { background: var(--coral); color: var(--bg); left: 3%; top: 22px; padding: 15px 12px; border-radius: 50%; font-size: 13px; transform: rotate(-13deg); }
.sticker--star { right: 2%; top: 23px; background: var(--lime); color: var(--bg); width: 100px; height: 100px; display: grid; place-content: center; gap: 2px; clip-path: polygon(50% 0%, 61% 27%, 90% 10%, 80% 40%, 100% 50%, 73% 61%, 90% 90%, 60% 79%, 50% 100%, 39% 72%, 10% 90%, 22% 60%, 0 50%, 28% 39%, 10% 10%, 40% 25%); font-size: 10px; transform: rotate(9deg); }
.art-note { position: absolute; bottom: 0; left: 16%; right: 9%; display: flex; justify-content: space-between; color: #8c829c; font-size: 9px; letter-spacing: 1px; }
.art-note span:last-child { display: flex; align-items: center; gap: 8px; }
.home-search { width: min(680px, 100%); margin: 0 auto; position: relative; z-index: 3; }
.search-box { width: 100%; min-height: 66px; display: flex; align-items: center; gap: 13px; padding: 9px 10px 9px 20px; background: #fff; border: 1px solid transparent; border-radius: 18px; box-shadow: 0 16px 55px #0002; transition: border .2s, box-shadow .2s; }
.search-box:focus-within { border-color: var(--lime); box-shadow: 0 0 0 4px #d9ff4520, 0 16px 55px #0002; }
.search-box__icon { color: #777080; flex-shrink: 0; }
.search-box input { min-width: 0; flex: 1; outline: none; border: 0; color: #211a2c; background: transparent; font-size: 14px; }
.search-box input::placeholder { color: #938b9b; }
.search-submit { display: grid; place-items: center; flex-shrink: 0; width: 46px; height: 46px; border: 0; border-radius: 13px; background: var(--lime); color: #171321; transition: transform .2s; }
.search-submit:hover { transform: rotate(8deg) scale(1.04); }
.icon-button { display: grid; place-items: center; border: 0; background: transparent; color: #7d7489; }
.search-hint { display: flex; justify-content: space-between; margin: 11px 8px 0; color: #7f768c; font-size: 10px; }
.search-hint span:first-child { letter-spacing: 1.3px; font-weight: 700; }
.category-pills { display: flex; justify-content: center; flex-wrap: wrap; gap: 9px; margin-top: 23px; }
.category-pills button { border: 1px solid #40364f; background: #211a2d; color: #d7d0e0; border-radius: 999px; padding: 10px 14px; font-size: 11px; transition: all .2s; }
.category-pills button:hover { border-color: var(--lime); color: var(--lime); transform: translateY(-2px); }
.manifesto { display: flex; align-items: center; justify-content: space-between; gap: 30px; padding: 38px max(24px, calc((100% - 1040px)/2)); background: var(--lime); color: var(--bg); position: relative; z-index: 1; }
.manifesto__left .eyebrow { color: #4a5120; }
.manifesto h2 { font-family: "Space Grotesk", sans-serif; font-size: clamp(42px, 6vw, 72px); line-height: .87; letter-spacing: -4px; margin: 17px 0 0; }
.manifesto h2 em { font-style: normal; color: #6550a2; }
.manifesto__right { max-width: 340px; display: flex; align-items: center; gap: 30px; }
.manifesto__right p { font-size: 15px; line-height: 1.65; }
.manifesto__right strong { font-size: 18px; }
.manifesto-arrow { width: 48px; height: 48px; border: 1px solid #17132155; border-radius: 50%; display: grid; place-items: center; flex-shrink: 0; }
.explore-section { width: min(1040px, calc(100% - 40px)); margin: 0 auto; padding: 76px 0 90px; }
.section-head { display: flex; justify-content: space-between; align-items: end; margin-bottom: 25px; }
.section-head h2 { font-family: "Space Grotesk", sans-serif; font-size: clamp(32px, 5vw, 55px); letter-spacing: -2.5px; line-height: 1; margin: 13px 0 0; }
.section-head h2 em { color: var(--lime); font-style: normal; }
.section-index { color: #756b82; font-size: 10px; letter-spacing: 1px; }
.explore-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 13px; }
.explore-tile { position: relative; height: 250px; overflow: hidden; border: 0; padding: 0; text-align: left; background: #33283e; color: white; border-radius: 4px; }
.explore-tile img { width: 100%; height: 100%; object-fit: cover; transition: transform .5s; filter: brightness(.72); }
.explore-tile:hover img { transform: scale(1.08); filter: brightness(.58); }
.tile-number { position: absolute; top: 14px; left: 14px; color: var(--lime); font-size: 10px; font-weight: 700; }
.tile-title { position: absolute; left: 14px; bottom: 17px; font-family: "Space Grotesk", sans-serif; font-weight: 700; font-size: 17px; }
.tile-arrow { position: absolute; right: 12px; bottom: 14px; display: grid; place-items: center; width: 30px; height: 30px; background: var(--lime); color: var(--bg); border-radius: 50%; }
.footer { border-top: 1px solid var(--line); min-height: 75px; width: min(1180px, calc(100% - 48px)); margin: 0 auto; display: flex; align-items: center; justify-content: space-between; gap: 16px; color: #7e748b; font-size: 9px; letter-spacing: 1px; }
.brand--small { font-size: 17px; }
.brand--small .brand-mark { width: 30px; height: 30px; border-radius: 9px; }
.results-page { width: min(1100px, calc(100% - 40px)); margin: 0 auto; min-height: 650px; }
.results-top { display: flex; align-items: center; gap: 22px; padding: 25px 0 17px; border-bottom: 1px solid var(--line); }
.results-top .search-box { max-width: 660px; min-height: 52px; border-radius: 14px; box-shadow: none; }
.results-top .search-submit { width: 36px; height: 36px; border-radius: 10px; }
.result-close { margin-left: auto; color: #b6adbf; }
.result-tabs { display: flex; gap: 25px; padding: 17px 0; border-bottom: 1px solid var(--line); color: #91889f; font-size: 12px; }
.result-tabs button { background: transparent; border: 0; color: inherit; }
.result-tabs .tab-active { color: var(--lime); position: relative; }
.result-tabs .tab-active::after { content: ""; position: absolute; bottom: -18px; left: 0; right: 0; height: 2px; background: var(--lime); }
.results-content { max-width: 900px; padding: 38px 0 70px; }
.results-heading { display: flex; align-items: end; justify-content: space-between; gap: 20px; margin-bottom: 23px; }
.results-heading h2 { font-family: "Space Grotesk", sans-serif; font-size: clamp(27px, 4vw, 42px); letter-spacing: -1.8px; margin: 9px 0 0; }
.results-heading h2 em { color: var(--lime); font-style: normal; }
.text-button { display: flex; align-items: center; gap: 7px; color: var(--lime); border: 0; background: transparent; font-size: 11px; padding: 8px 0; }
.ai-summary { padding: 22px 24px; border: 1px solid #57456a; border-radius: 16px; background: linear-gradient(120deg, #2b203b, #211a2e); margin-bottom: 30px; }
.ai-summary__top { display: flex; justify-content: space-between; align-items: center; color: var(--lime); font-size: 10px; font-weight: 700; letter-spacing: 1px; }
.ai-summary__top span:first-child { display: flex; align-items: center; gap: 7px; }
.demo-tag { color: #b8a8cc; border: 1px solid #57456a; padding: 4px 7px; border-radius: 4px; font-size: 8px; }
.ai-summary h3 { font-family: "Space Grotesk", sans-serif; font-size: 22px; margin: 17px 0 8px; }
.ai-summary p { color: #b8afc5; font-size: 12px; line-height: 1.7; max-width: 700px; margin: 0; }
.result-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 15px; }
.food-card { border: 1px solid #3a3048; background: #211a2c; border-radius: 13px; overflow: hidden; transition: transform .2s, border-color .2s; }
.food-card:hover { transform: translateY(-3px); border-color: #75608c; }
.food-card__image-wrap { height: 170px; position: relative; overflow: hidden; }
.food-card__image { width: 100%; height: 100%; object-fit: cover; }
.food-card__category { position: absolute; left: 12px; top: 12px; padding: 6px 9px; border-radius: 999px; background: var(--lime); color: var(--bg); font-size: 9px; font-weight: 700; }
.food-card__open { position: absolute; right: 12px; top: 12px; width: 30px; height: 30px; display: grid; place-items: center; background: #171321d9; color: white; border: 0; border-radius: 50%; }
.food-card__body { padding: 15px; }
.food-card__body h3 { margin: 0 0 7px; font-family: "Space Grotesk", sans-serif; font-size: 17px; }
.food-card__body p { margin: 0; color: #a69caf; font-size: 11px; line-height: 1.65; }
.food-card__facts { display: flex; gap: 13px; margin-top: 13px; color: var(--lime); font-size: 10px; }
.food-card__facts span { display: flex; align-items: center; gap: 5px; }
.empty-state { text-align: center; padding: 50px 20px; color: #a69caf; }
.empty-state > span { color: var(--lime); font-size: 28px; }
.empty-state h3 { color: white; font-family: "Space Grotesk", sans-serif; font-size: 24px; margin: 15px 0 8px; }
.empty-state p { font-size: 12px; }
.loading-state { display: flex; align-items: center; justify-content: center; gap: 10px; padding: 50px; color: #b5a9c5; font-size: 12px; }
.loader { width: 18px; height: 18px; border: 2px solid #51445f; border-top-color: var(--lime); border-radius: 50%; animation: spin .7s linear infinite; }
.error-message { color: #ff8d7a; font-size: 12px; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 700px) {
  .navbar { height: 70px; width: calc(100% - 32px); }
  .nav-links { gap: 17px; font-size: 11px; }
  .hero { padding-top: 49px; width: calc(100% - 32px); }
  .hero h1 { letter-spacing: -3px; font-size: clamp(43px, 12vw, 70px); }
  .hero-subline { gap: 7px; }
  .hero-subline p { font-size: 16px; width: 100%; }
  .hero-subline span { font-size: 11px; }
  .hero-art { height: 245px; margin-top: 25px; }
  .photo--main { width: 72%; height: 205px; left: 10%; }
  .photo--small { width: 34%; height: 115px; right: 1%; bottom: 5px; }
  .sticker--tomato { left: 0; top: 14px; font-size: 9px; padding: 11px 9px; }
  .sticker--star { width: 72px; height: 72px; right: 0; top: 12px; font-size: 8px; }
  .art-note { left: 10%; right: 1%; font-size: 7px; }
  .search-box { min-height: 58px; padding-left: 14px; gap: 9px; }
  .search-box input { font-size: 12px; }
  .search-submit { width: 40px; height: 40px; }
  .category-pills { gap: 7px; }
  .category-pills button { padding: 9px 11px; font-size: 10px; }
  .manifesto { padding: 32px 20px; align-items: start; flex-direction: column; gap: 16px; }
  .manifesto h2 { font-size: 55px; }
  .manifesto__right { max-width: none; width: 100%; justify-content: space-between; }
  .explore-section { padding: 54px 0 60px; width: calc(100% - 32px); }
  .section-head h2 { font-size: 35px; letter-spacing: -1.7px; }
  .explore-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 9px; }
  .explore-tile { height: 190px; }
  .tile-title { font-size: 14px; left: 10px; bottom: 12px; }
  .tile-arrow { right: 8px; bottom: 8px; width: 26px; height: 26px; }
  .footer { width: calc(100% - 32px); flex-wrap: wrap; padding: 18px 0; }
  .results-top { gap: 10px; flex-wrap: wrap; }
  .results-top .brand { font-size: 15px; }
  .results-top .search-box { order: 3; flex-basis: 100%; max-width: none; }
  .results-heading { align-items: start; flex-direction: column; }
  .result-grid { grid-template-columns: 1fr; }
  .results-content { padding-top: 28px; }
  .result-tabs { gap: 17px; font-size: 11px; overflow-x: auto; }
  .ai-summary { padding: 17px; }
}
''',
".env.example": r'''# Set this when the FastAPI backend is running, e.g. http://localhost:8000
VITE_API_URL=
''',
"README.md": r'''# BITBYTE frontend

React + TypeScript + Vite frontend for the BITBYTE food search experience.

## Run

```bash
npm install
npm run dev
```

## Current search behavior

- Search is functional using a small local demo dataset.
- Search results are ranked by title, tags, category and description.
- To connect a backend, set `VITE_API_URL` in `.env.local`.
- Expected backend endpoint: `GET /api/search?q=<query>`
- Expected response shape:

```json
{
  "query": "paneer",
  "total": 1,
  "results": [
    {
      "id": "paneer",
      "title": "Paneer",
      "category": "Nutrition",
      "description": "Food description",
      "image": "https://example.com/image.jpg",
      "tags": ["paneer", "protein"],
      "calories": 265,
      "protein": 18
    }
  ]
}
```

Demo data is not authoritative nutrition guidance. Real nutrition values and source citations will be connected in the backend phase.
'''
}
# fix placeholder image to valid unsplash URL
files["src/data/food.ts"] = files["src/data/food.ts"].replace("https://images.unsplash.com/photo-157 (placeholder)", "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=900&q=85")
os.makedirs(root, exist_ok=True)
for path, content in files.items():
    full=os.path.join(root,path)
    os.makedirs(os.path.dirname(full),exist_ok=True)
    with open(full,"w",encoding="utf-8") as f: f.write(content)
zip_path = os.path.expanduser("~/BITBYTE/bitbyte_frontend_starter.zip")
with zipfile.ZipFile(zip_path,"w",zipfile.ZIP_DEFLATED) as z:
    for path in files:
        z.write(os.path.join(root,path), f"bitbyte-frontend/{path}")
print(zip_path, len(files))
