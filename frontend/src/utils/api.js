// src/utils/api.js
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export const loginUser = async (data, rememberMe) => {
  try {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })

    const responseData = await response.json()

    if (!response.ok) {
      throw new Error(responseData.detail || 'Login failed')
    }

    const storage = rememberMe ? localStorage : sessionStorage
    storage.setItem('authToken', responseData.access_token)

    return responseData.access_token
  } catch (error) {
    throw new Error(error.message)
  }
}
