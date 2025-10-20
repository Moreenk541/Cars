"use client"

import { resolve } from "path"
import type React from "react"
import {createContext,useContext, useState,useEffect} from "react"

interface User {
    id: number
    username :string
    email: string
    is_admin: boolean

}

interface AuthContextType {
    user :User |null
    login: (email : string , password:string) => Promise<boolean>
    signup:(username:string, email:string,password:string) =>Promise<boolean>
    logout:()=>Promise<void>
    loading:boolean
}

const AuthContext =createContext<AuthContextType | undefined>(undefined)

const API_BASE_URL =process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"

export function AuthProvider({children}:{children:React.ReactNode}){
    const [user,setUser] = useState<User |null>(null)
    const[loading,setLoading] = useState(true)

    useEffect(()=>{
        checkAuthStatus()
    },[])

    const checkAuthStatus =async () => {
        try{
            const token = localStorage.getItem("token")
            if (token) {
                const response = await fetch(`${API_BASE_URL}/api/auth/me`,{
                    headers:{
                        Authorization:`Bearer ${token}`,
                        "Content-Type":"application/json"
                    },
                })
                if (response.ok){
                    const userData = await response.json()
                    setUser(userData)
                } else {
                    //token invalid? remove it
                    localStorage.removeItem("token")
                    localStorage.removeItem("user")
                }


            }
        } catch (error){
            console.error("Auth check failed:",error)
            //Fallback to localstorage for offline mode

            const savedUser =localStorage.getItem("user")
            if (savedUser){
                setUser(JSON.parse(savedUser))
            }

        } finally{
            setLoading(false)
        }
    }

    const login = async (email:string,password:string): Promise<boolean> =>{
        try{
            const response = await fetch(`${API_BASE_URL}/api/auth/login`,{
                method:"POST",
                headers:{
                    "Content-Type":"applicatio/json",
                },
                body:JSON.stringify({email,password}),
            })

            if (!response.ok){
                const errorData = await response.json()
                throw new Error(errorData.message || "Login failed")
            }

            const data = await response.json()


            //Store token and user data

            localStorage.setItem("token",data.token)
            localStorage.setItem("User",JSON.stringify(data.user))
            setUser(data.user)

            return true
        } catch (error){
            console.error("Login failed:",error)

        }
        return false
    }

    const signup =async (username:string,email:string,password:string):Promise<boolean> =>{
        try{
            const response = await fetch(`${API_BASE_URL}/api/auth/signup`,{
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                },
                body:JSON.stringify({username,email,password}),
            })

            if (!response.ok){
                const errorData = await response.json()
                throw new Error(errorData.message || "Signup failed")
            }

            return true
        }catch (error) {
            console.log("Signup failed:",error)
            return false
        }
    }



    const logout = async () =>{
        try{
            const token = localStorage.getItem("token")

            if (token){
                await fetch(`${API_BASE_URL}/api/auth/logout`,{
                    method: "POST",
                    headers:{
                        "Content-Type": "application/json",
                    },

                })

            }

        }catch (error){
            console.error("Logout API call failed:", error)
        } finally{
            //clear local storage
            setUser(null)
            localStorage.removeItem("token")
            localStorage.removeItem("user")
        }
    }


    return <AuthContext.Provider value={{ user, login, signup, logout, loading }}>{children}</AuthContext.Provider>
}

export function useAuth(){
    const context = useContext(AuthContext)
    if (context === undefined){
        throw new Error("useAuth must be used within an AuthProvider")
    }
    return context
}






 

