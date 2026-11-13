import { ArrowDownRight, ArrowRight, Camera, Heart, LoaderCircle, MessageCircle, Send, Sparkles, Utensils, X } from 'lucide-react'
import { useEffect, useMemo, useRef, useState } from 'react'
import SearchBar from './components/SearchBar'
import FoodCard from './components/FoodCard'
import { foodData } from './data/food'
import { analyzeMeal, askFoodAssistant, createMealPlan, searchFoods } from './services/search'
import type { FoodResult } from './types'

type ChatMessage = { role: 'user' | 'assistant'; content: string }
type Profile = { name: string; preferences: string; saved: FoodResult[]; plan: string }
const PROFILE_KEY = 'bitbyte-profile-v1'
const CHAT_KEY = 'bitbyte-chat-v1'
const initialProfile: Profile = { name: '', preferences: '', saved: [], plan: '' }
const categories = [
  { label: '🥑 Nutrition', query: 'nutrition' }, { label: '🍜 Recipes', query: 'chicken' },
  { label: '🥩 Protein', query: 'protein' }, { label: '🍓 Ingredients', query: 'ingredient' }, { label: '🍕 Food science', query: 'food science' },
]

function readProfile(): Profile {
  try { return { ...initialProfile, ...JSON.parse(localStorage.getItem(PROFILE_KEY) || '{}') } } catch { return initialProfile }
}
function readChat(): ChatMessage[] {
  try { return JSON.parse(localStorage.getItem(CHAT_KEY) || '[]') } catch { return [] }
}

export default function App() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<FoodResult[]>([])
  const [summary, setSummary] = useState('')
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [hasMore, setHasMore] = useState(false)
  const [warnings, setWarnings] = useState<string[]>([])
  const [searched, setSearched] = useState(false)
  const [loading, setLoading] = useState(false)
  const [loadingMore, setLoadingMore] = useState(false)
  const [error, setError] = useState('')
  const [profile, setProfile] = useState<Profile>(readProfile)
  const [profileOpen, setProfileOpen] = useState(false)
  const [assistantOpen, setAssistantOpen] = useState(false)
  const [chat, setChat] = useState<ChatMessage[]>(readChat)
  const [chatInput, setChatInput] = useState('')
  const [chatBusy, setChatBusy] = useState(false)
  const [scanBusy, setScanBusy] = useState(false)
  const [scanResult, setScanResult] = useState('')
  const [goal, setGoal] = useState('Balanced meals')
  const [planBusy, setPlanBusy] = useState(false)
  const fileRef = useRef<HTMLInputElement>(null)
  const chatEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => { localStorage.setItem(PROFILE_KEY, JSON.stringify(profile)) }, [profile])
  useEffect(() => { localStorage.setItem(CHAT_KEY, JSON.stringify(chat.slice(-30))) }, [chat])
  useEffect(() => { chatEndRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [chat, assistantOpen])

  async function runSearch(value: string) {
    setQuery(value); setSearched(true); setLoading(true); setLoadingMore(false); setError(''); setResults([]); setSummary(''); setPage(1)
    try {
      const response = await searchFoods(value)
      setResults(response.results); setSummary(response.summary || ''); setTotal(response.total); setHasMore(Boolean(response.hasMore)); setPage(response.page || 1); setWarnings(response.warnings || [])
    } catch { setError('Search could not be completed. Check the backend connection and try again.'); setResults([]) }
    finally { setLoading(false) }
  }

  async function loadMore() {
    if (loadingMore || !hasMore) return
    setLoadingMore(true)
    try {
      const response = await searchFoods(query, page + 1)
      setResults((current) => [...current, ...response.results]); setPage(response.page || page + 1); setHasMore(Boolean(response.hasMore)); setTotal(response.total); setWarnings(response.warnings || [])
    } catch { setError('Could not load the next page. Try again.') }
    finally { setLoadingMore(false) }
  }

  function resetSearch() { setQuery(''); setResults([]); setSummary(''); setSearched(false); setError(''); setWarnings([]) }
  function toggleSave(item: FoodResult) {
    setProfile((current) => ({ ...current, saved: current.saved.some((saved) => saved.id === item.id) ? current.saved.filter((saved) => saved.id !== item.id) : [item, ...current.saved] }))
  }
  const savedIds = useMemo(() => new Set(profile.saved.map((item) => item.id)), [profile.saved])

  async function sendChat(message = chatInput) {
    const text = message.trim(); if (!text || chatBusy) return
    const previous = chat.slice(-12)
    setChat((current) => [...current, { role: 'user', content: text }]); setChatInput(''); setChatBusy(true)
    try {
      const context = [profile.preferences ? `User food preferences and restrictions: ${profile.preferences}` : '', query ? `Current food search: ${query}. Search overview: ${summary}. Results: ${results.slice(0, 12).map((item) => item.title).join(', ')}` : ''].filter(Boolean).join('\n')
      const reply = await askFoodAssistant(text, previous, context)
      setChat((current) => [...current, { role: 'assistant', content: reply }])
    } catch (e) { setChat((current) => [...current, { role: 'assistant', content: e instanceof Error ? e.message : 'The food assistant is unavailable right now.' }]) }
    finally { setChatBusy(false) }
  }

  async function scanPhoto(file?: File) {
    if (!file) return
    if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type) || file.size > 9 * 1024 * 1024) { setScanResult('Please choose a JPEG, PNG, or WebP image under 9 MB.'); return }
    setScanBusy(true); setScanResult('Analyzing the meal photo…')
    try {
      const base64 = await new Promise<string>((resolve, reject) => { const reader = new FileReader(); reader.onload = () => resolve(String(reader.result).split(',')[1]); reader.onerror = reject; reader.readAsDataURL(file) })
      const analysis = await analyzeMeal(base64, file.type)
      const nutrients = [`Estimated calories: ${analysis.estimatedCalories ?? 'unknown'} kcal`, `Protein: ${analysis.estimatedProteinGrams ?? 'unknown'} g`, `Carbs: ${analysis.estimatedCarbsGrams ?? 'unknown'} g`, `Fat: ${analysis.estimatedFatGrams ?? 'unknown'} g`].join(' · ')
      const report = `Likely foods: ${(analysis.foods || []).join(', ') || 'could not confidently identify'}\n${nutrients}\nConfidence: ${analysis.confidence || 'low'}\n${analysis.notes || ''}`
      setScanResult(report); setChat((current) => [...current, { role: 'assistant', content: report }])
    } catch (e) { setScanResult(e instanceof Error ? e.message : 'Photo analysis failed. Check that Ollama and qwen2.5vl:7b are running.') }
    finally { setScanBusy(false); if (fileRef.current) fileRef.current.value = '' }
  }

  async function generatePlan() {
    setPlanBusy(true)
    try { const plan = await createMealPlan(goal, profile.preferences); setProfile((current) => ({ ...current, plan })) }
    catch (e) { setProfile((current) => ({ ...current, plan: e instanceof Error ? e.message : 'Could not create a plan. Check the model connection.' })) }
    finally { setPlanBusy(false) }
  }

  const suggestion = query ? `Try asking: “How could I use ${query} in a balanced meal?”` : 'Try asking for a quick high-protein breakfast or a recipe with what you have.'

  return (
    <main className="site-shell">
      <div className="ambient ambient--one" /><div className="ambient ambient--two" />
      <header className="navbar">
        <a className="brand" href="/" onClick={(e) => { e.preventDefault(); resetSearch() }}><span className="brand-mark"><Utensils size={19} strokeWidth={2.7} /></span><span>BITBYTE<span className="brand-dot">.</span></span></a>
        <nav className="nav-links" aria-label="Main navigation"><a href="#discover">Discover</a><a href="#recipes" onClick={() => runSearch('chicken')}>Recipes</a><button onClick={() => { setProfileOpen(true); setAssistantOpen(false) }}>My food space</button></nav>
        <button className="nav-avatar" aria-label="Open user profile" onClick={() => setProfileOpen(true)}>{profile.name.trim().charAt(0).toUpperCase() || 'B'}</button>
      </header>

      {!searched ? <section className="hero">
        <div className="hero-kicker"><span className="kicker-dot" /> THE FOOD UNIVERSE <span className="kicker-line" /></div>
        <h1>FOOD IS MORE<br /><span>THAN JUST FOOD.</span></h1>
        <div className="hero-subline"><p>Explore. Eat. Understand.</p><span>Your curiosity deserves a better search engine.</span></div>
        <div className="hero-art"><div className="art-sticker sticker--tomato">TASTE<br />THE<br />WORLD</div><div className="art-sticker sticker--star"><Sparkles size={27} /> GOOD<br />FOOD<br />ENERGY</div>
          <div className="food-photo photo--main"><img src="https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1200&q=90" alt="Colourful food spread" /><span className="photo-label">A LITTLE BIT OF EVERYTHING</span></div>
          <div className="food-photo photo--small"><img src="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=700&q=85" alt="Fresh salad bowl" /></div>
          <div className="art-note"><span>01 / 05</span><span>DISCOVER SOMETHING DELICIOUS <ArrowDownRight size={14} /></span></div></div>
        <div className="home-search"><SearchBar onSearch={runSearch} /><div className="search-hint"><span>TRY SEARCHING</span><span>anything edible, really ↗</span></div></div>
        <div className="category-pills">{categories.map((category) => <button key={category.label} onClick={() => runSearch(category.query)}>{category.label}</button>)}</div>
      </section> : <section className="results-page">
        <div className="results-top"><a className="brand brand--small" href="/" onClick={(e) => { e.preventDefault(); resetSearch() }}><span className="brand-mark"><Utensils size={17} /></span><span>BITBYTE<span className="brand-dot">.</span></span></a><SearchBar initialValue={query} compact onSearch={runSearch} /><button className="icon-button result-close" onClick={resetSearch} aria-label="Back to home"><X size={19} /></button></div>
        <div className="result-tabs"><span className="tab-active">All results</span><button onClick={() => runSearch(`${query} nutrition`)}>Nutrition</button><button onClick={() => runSearch(`${query} recipe`)}>Recipes</button><button onClick={() => runSearch(`${query} protein`)}>Protein</button><button onClick={() => setProfileOpen(true)}>Saved ({profile.saved.length})</button></div>
        <div className="results-content"><div className="results-heading"><div><span className="eyebrow">SEARCHING THE FOOD UNIVERSE</span><h2>Results for <em>“{query}”</em></h2><span className="result-count">{total.toLocaleString()} food results · recipes shown where available</span></div><button className="text-button" onClick={resetSearch}>New search <ArrowRight size={15} /></button></div>
          {summary && <div className="ai-summary"><div className="ai-summary__top"><span><Sparkles size={15} /> BITBYTE AI OVERVIEW</span><span className="demo-tag">QWEN</span></div><h3>A quick guide to {query}</h3><p>{summary}</p></div>}
          {warnings.map((warning) => <p className="warning-message" key={warning}>{warning}</p>)}{error && <p className="error-message">{error}</p>}
          {loading ? <div className="loading-state"><span className="loader" /> Searching food and recipe sources…</div> : results.length ? <><div className="result-grid">{results.map((item) => <FoodCard key={item.id} item={item} saved={savedIds.has(item.id)} onSave={() => toggleSave(item)} />)}</div>{hasMore && <button className="load-more" onClick={loadMore} disabled={loadingMore}>{loadingMore ? <LoaderCircle className="spin-icon" size={17} /> : null}{loadingMore ? 'Loading more results…' : 'Load more food results'}</button>}</> : <div className="empty-state"><span>¯\_(ツ)_/¯</span><h3>No food found. Yet.</h3><p>Try “paneer”, “protein”, “oats” or “lentils”.</p></div>}
        </div></section>}

      {!searched && <><section className="manifesto" id="discover"><div className="manifesto__left"><span className="eyebrow">BITBYTE INTELLIGENCE <Sparkles size={14} /></span><h2>EAT<br /><em>SMARTER.</em></h2></div><div className="manifesto__right"><p>Not another recipe website.<br /><strong>A whole new way to explore food.</strong></p><span className="manifesto-arrow"><ArrowRight size={25} /></span></div></section>
        <section className="explore-section" id="recipes"><div className="section-head"><div><span className="eyebrow">A WORLD ON YOUR PLATE</span><h2>Explore the delicious <em>chaos.</em></h2></div><span className="section-index">01 — 04</span></div><div className="explore-grid">{foodData.slice(0, 4).map((item, index) => <button className={`explore-tile explore-tile--${index + 1}`} key={item.id} onClick={() => runSearch(item.title)}><img src={item.image} alt="" loading="lazy" /><span className="tile-number">0{index + 1}</span><span className="tile-title">{['Food discovery', 'Nutrition explorer', 'Recipe universe', 'Ingredient library'][index]}</span><span className="tile-arrow"><ArrowRight size={17} /></span></button>)}</div></section></>}
      <footer className="footer"><a className="brand brand--small" href="#" onClick={(e) => { e.preventDefault(); resetSearch() }}>BITBYTE<span className="brand-dot">.</span></a><span>MADE FOR THE CURIOUS & HUNGRY.</span><span>© BITBYTE 2026</span></footer>

      <aside className={`ai-dock ${assistantOpen ? 'ai-dock--open' : ''}`} aria-label="BITBYTE food assistant">
        {assistantOpen ? <div className="assistant-panel"><div className="assistant-head"><div><span className="assistant-online" /><strong>BITBYTE food assistant</strong><small>Powered by Qwen vision</small></div><button onClick={() => setAssistantOpen(false)} aria-label="Close assistant"><X size={18} /></button></div>
          <div className="assistant-suggestion"><Sparkles size={15} /><span>{suggestion}</span><button onClick={() => sendChat(suggestion.replace('Try asking: ', '').replace(/[“”]/g, ''))}>Ask</button></div>
          <div className="chat-messages">{chat.length === 0 && <p className="chat-welcome">Ask about ingredients, recipes, nutrition, or meal routines. Your recent chat stays on this device.</p>}{chat.map((message, index) => <div className={`chat-message chat-message--${message.role}`} key={index}>{message.content}</div>)}{chatBusy && <div className="chat-message chat-message--assistant"><LoaderCircle className="spin-icon" size={16} /> Thinking…</div>}{scanResult && <div className="scan-result">{scanResult}</div>}<div ref={chatEndRef} /></div>
          <div className="assistant-actions"><button className="scan-button" onClick={() => fileRef.current?.click()} disabled={scanBusy}><Camera size={16} /> {scanBusy ? 'Analyzing…' : 'Scan a meal'}</button><input ref={fileRef} type="file" accept="image/jpeg,image/png,image/webp" hidden onChange={(e) => scanPhoto(e.target.files?.[0])} /></div>
          <form className="chat-form" onSubmit={(e) => { e.preventDefault(); void sendChat() }}><input value={chatInput} onChange={(e) => setChatInput(e.target.value)} placeholder="Ask anything about food…" aria-label="Message the food assistant" /><button aria-label="Send message" disabled={chatBusy || !chatInput.trim()}><Send size={17} /></button></form>
        </div> : <><div className="dock-tip"><Sparkles size={15} /><span><b>Food idea</b>{suggestion}</span></div><button className="assistant-launch" onClick={() => setAssistantOpen(true)}><MessageCircle size={18} /> Ask BITBYTE</button></>}
      </aside>

      {profileOpen && <div className="modal-backdrop" onMouseDown={(e) => { if (e.target === e.currentTarget) setProfileOpen(false) }}><section className="profile-panel"><header className="profile-head"><div><span className="eyebrow">YOUR FOOD SPACE</span><h2>Profile & plans</h2></div><button className="icon-button" onClick={() => setProfileOpen(false)} aria-label="Close profile"><X /></button></header>
        <label className="field-label">Name<input value={profile.name} onChange={(e) => setProfile((p) => ({ ...p, name: e.target.value }))} placeholder="What should we call you?" /></label>
        <label className="field-label">Food preferences, allergies, or restrictions<textarea value={profile.preferences} onChange={(e) => setProfile((p) => ({ ...p, preferences: e.target.value }))} placeholder="For example: vegetarian, peanuts allergy, quick weekday meals" rows={3} /></label>
        <div className="plan-controls"><label className="field-label">Planning goal<input value={goal} onChange={(e) => setGoal(e.target.value)} /></label><button className="plan-button" onClick={generatePlan} disabled={planBusy}>{planBusy ? 'Making your plan…' : 'Create AI meal plan'}</button></div>
        {profile.plan && <div className="meal-plan"><div className="panel-subhead"><h3>Your meal plan</h3><button onClick={() => setProfile((p) => ({ ...p, plan: '' }))}>Clear</button></div><pre>{profile.plan}</pre></div>}
        <div className="saved-section"><h3><Heart size={16} /> Saved recipes & foods <span>{profile.saved.length}</span></h3>{profile.saved.length ? profile.saved.map((item) => <div className="saved-item" key={item.id}><div><strong>{item.title}</strong><small>{item.category} · {item.source || 'BITBYTE'}</small></div><button onClick={() => toggleSave(item)}>Remove</button></div>) : <p className="muted-copy">Save an item from your search results to keep it here.</p>}</div>
        <p className="local-note">This profile and its saved items are stored in this browser. Sign-in and cross-device sync are not configured.</p>
      </section></div>}
    </main>
  )
}
