import type { FoodResult } from '../types'

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
    image: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=900&q=85',
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
}