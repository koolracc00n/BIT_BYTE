import { ArrowUpRight, Flame, Heart, Tags } from 'lucide-react'
import type { FoodResult } from '../types'

export default function FoodCard({ item, saved = false, onSave }: { item: FoodResult; saved?: boolean; onSave?: () => void }) {
  return (
    <article className="food-card">
      <div className="food-card__image-wrap">
        {item.image ? <img src={item.image} alt="" className="food-card__image" loading="lazy" /> : <div className="food-card__placeholder"><span>BITBYTE</span><strong>{item.title.slice(0, 1).toUpperCase()}</strong></div>}
        <span className="food-card__category">{item.category}</span>
        {item.url && <a className="food-card__open" href={item.url} target="_blank" rel="noreferrer" aria-label={`Open ${item.title}`}>
          <ArrowUpRight size={18} />
        </a>}
        {onSave && <button className={`food-card__save ${saved ? 'is-saved' : ''}`} onClick={onSave} aria-label={saved ? `Remove ${item.title} from saved` : `Save ${item.title}`}><Heart size={16} fill={saved ? 'currentColor' : 'none'} /></button>}
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
        {item.source && <span className="food-card__source">Source: {item.source}</span>}
      </div>
    </article>
  )
}
