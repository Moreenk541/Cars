const  API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

interface ApiResponse<T> {
  data: T
  message?: string
  error?: string
}

class ApiClient {
    private baseURL: string


    constructor(baseURL:string){
        this.baseURL = baseURL
    }

    private async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
        const url =`${this.baseURL}${endpoint}`
        const token =localStorage.getItem("token")

        const config: RequestInit ={
            headers :{
                "Content-Type":"application/json",
                ...(token && {Authorization: `Bearer ${token}`}),
               ...options.headers,


            },
            ...options,
        }

        try{
            const response = await fetch(url,config)
            const data = await response.json()

            if (!response.ok){
                throw new Error(data.message || `HTTP error! status: ${response.status}`)
            }

            return {data}
        }
        catch (error){
            console.error(`API request failed: ${endpoint}`, error)
            return { error: error instanceof Error ? error.message : "Unknown error" }

        }
    }

}

export const apiClient = new ApiClient(API_BASE_URL)
export default apiClient

