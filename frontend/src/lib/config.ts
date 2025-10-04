export const config = {
  // API Configuration
  apiUrl: process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000",
  isDevelopment: process.env.NODE_ENV === "development",
  isProduction: process.env.NODE_ENV === "production",




  // Request Configuration
  request: {
    timeout: 10000, // 10 seconds
    retries: 3,
  },

  // Local Storage Keys
  storage: {
    token: "token",
    user: "user",
    cart: (userId: number) => `cart_${userId}`,
    registeredUsers: "registeredUsers",
  },

 

} as const
export default config
