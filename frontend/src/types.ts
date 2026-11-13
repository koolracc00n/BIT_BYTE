export type FoodCategory = 'Nutrition' | 'Recipes' | 'Protein' | 'Ingredients' | 'Food science'

export interface FoodResult {
  id: string
  title: string
  category: FoodCategory
  description: string
  image: string
  tags: string[]
  calories?: number
  protein?: number
  fat?: number
  carbs?: number
  source?: string
  url?: string
}

export interface SearchResponse {
  query: string
  total: number
  results: FoodResult[]
  summary?: string
  page?: number
  pageSize?: number
  hasMore?: boolean
  warnings?: string[]
}
