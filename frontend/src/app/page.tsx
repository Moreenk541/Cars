"use client"

import { useState } from "react"
import { AuthProvider, useAuth } from "@/components/auth/auth-context"
import { CartProvider } from "@/components/cart/cart-context"
import { Header } from "@/components/layout/header"
import { LoginForm } from "@/components/auth/login-form"
import { SignupForm } from "@/components/auth/signup-form"
import { VehicleGrid } from "@/components/vehicles/vehicle-grid"
import { VehicleDetailsComponent } from "@/components/vehicles/vehicle-details"
import { CheckoutModal } from "@/components/cart/checkout-modal"
import { Dashboard } from "@/components/dashboard/dashboard"

function MainContent() {
  const [showAuth, setShowAuth] = useState(false)
  const [authMode, setAuthMode] = useState<"login" | "signup">("login")
  const [selectedVehicleId, setSelectedVehicleId] = useState<number | null>(null)
  const [showCheckout, setShowCheckout] = useState(false)
  const [showDashboard, setShowDashboard] = useState(false)
  const { user } = useAuth()

  const handleAuthClick = () => {
    setShowAuth(true)
  }

  const toggleAuthMode = () => {
    setAuthMode(authMode === "login" ? "signup" : "login")
  }

  const handleViewDetails = (vehicleId: number) => {
    setSelectedVehicleId(vehicleId)
  }

  const handleBackToListings = () => {
    setSelectedVehicleId(null)
  }

  const handleCheckout = () => {
    if (!user) {
      setShowAuth(true)
      setAuthMode("login")
      return
    }
    setShowCheckout(true)
  }

  const handleDashboard = () => {
    if (!user) {
      setShowAuth(true)
      setAuthMode("login")
      return
    }
    setShowDashboard(true)
    setSelectedVehicleId(null)
  }

  const handleBackToHome = () => {
    setShowDashboard(false)
    setSelectedVehicleId(null)
  }

  if (showAuth) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100vh-200px)]">
        <div className="w-full max-w-md">
          <div className="mb-4 text-center">
            <button onClick={() => setShowAuth(false)} className="text-sm text-muted-foreground hover:text-foreground">
              ← Continue browsing without account
            </button>
          </div>
          {authMode === "login" ? (
            <LoginForm onToggleMode={toggleAuthMode} onSuccess={() => setShowAuth(false)} />
          ) : (
            <SignupForm onToggleMode={toggleAuthMode} onSuccess={() => setShowAuth(false)} />
          )}
        </div>
      </div>
    )
  }

  if (showDashboard && user) {
    return (
      <>
        <div className="mb-6">
          <button onClick={handleBackToHome} className="text-primary hover:text-primary/80 transition-colors">
            ← Back to Marketplace
          </button>
        </div>
        <Dashboard />
      </>
    )
  }

  if (selectedVehicleId) {
    return <VehicleDetailsComponent vehicleId={selectedVehicleId} onBack={handleBackToListings} />
  }

  return (
    <>
      <div className="space-y-8">
        <div className="text-center py-8">
          <h1 className="text-3xl font-bold mb-2">
            {user ? `Welcome back, ${user.username}!` : "Find Your Perfect Car"}
          </h1>
          <p className="text-muted-foreground">
            {user ? "Browse our collection of premium vehicles" : "Discover premium vehicles from trusted sellers"}
          </p>
        </div>
        <VehicleGrid onViewDetails={handleViewDetails} />
      </div>
      <CheckoutModal isOpen={showCheckout} onClose={() => setShowCheckout(false)} />
    </>
  )
}

export default function HomePage() {
  return (
    <AuthProvider>
      <CartProvider>
        <div className="min-h-screen bg-background">
          <Header onAuthClick={() => {}} onCheckout={() => {}} onDashboard={() => {}} />
          <main className="container mx-auto px-4 py-8">
            <MainContent />
          </main>
        </div>
      </CartProvider>
    </AuthProvider>
  )
}
