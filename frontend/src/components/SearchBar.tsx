import { ArrowUp, Search, X } from 'lucide-react'
import { useState } from 'react'
import type { FormEvent } from 'react'

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
}
