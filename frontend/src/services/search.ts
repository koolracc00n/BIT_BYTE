
import axios from 'axios'
import type { SearchResponse } from '../types'
import { searchFood } from '../data/food'

const API_BASE_URL = import.meta.env.VITE_API_URL

export async function searchFoods(query: string, page = 1): Promise<SearchResponse> {
  if (API_BASE_URL) {
    const response = await axios.get(`${API_BASE_URL}/api/search`, {
      params: { query, page, pageSize: 50 },
    })

    return {
      query: response.data.query,
      total: response.data.totalHits,
      results: response.data.results,
      summary: response.data.summary,
      page: response.data.page,
      pageSize: response.data.pageSize,
      hasMore: response.data.hasMore,
      warnings: response.data.warnings,
    }
  }

  const results = searchFood(query)

  return {
    query,
    total: results.length,
    results,
    summary: undefined,
    hasMore: false,
  }
}

export async function askFoodAssistant(message: string, history: Array<{role: 'user'|'assistant'; content: string}>, context = '') {
  const response = await axios.post(`${API_BASE_URL || 'http://localhost:5000'}/api/search/chat`, { message, history, context })
  return response.data.reply as string
}

export async function createMealPlan(goal: string, preferences: string, days = 7) {
  const response = await axios.post(`${API_BASE_URL || 'http://localhost:5000'}/api/search/plan`, { goal, preferences, days })
  return response.data.plan as string
}

export async function analyzeMeal(image: string, mimeType: string) {
  const response = await axios.post(`${API_BASE_URL || 'http://localhost:5000'}/api/search/image`, { image, mimeType }, { timeout: 190_000 })
  return response.data.analysis as { foods?: string[]; estimatedCalories?: number|null; estimatedProteinGrams?: number|null; estimatedCarbsGrams?: number|null; estimatedFatGrams?: number|null; confidence?: string; notes?: string }
}
