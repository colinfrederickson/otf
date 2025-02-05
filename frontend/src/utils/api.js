// src/utils/api.js
export const loginUser = async (data, rememberMe) => {
  try {
    const response = await fetch('http://localhost:8000/api/login', {
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
