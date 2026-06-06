import { useEffect } from 'react'
import { useAuthStore } from '@/stores/authStore'
import api from '@/lib/api'

export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const user = useAuthStore((state) => state.user)
  const setUser = useAuthStore((state) => state.setUser)
  const logout = useAuthStore((state) => state.logout)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token && !user) {
      // Verify token and load user
      api
        .get('/api/auth/me')
        .then((response) => setUser(response.data))
        .catch(() => logout())
    }
  }, [user, setUser, logout])

  if (!user) {
    return null
  }

  // Block access if user is pending approval
  if (user.status === 'pending') {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="bg-card border border-border/50 rounded-xl p-8 max-w-md mx-auto text-center">
          <h1 className="text-2xl font-bold text-foreground mb-4">Pending Approval</h1>
          <p className="text-muted mb-4">
            Your account is awaiting administrator approval. Please check back soon.
          </p>
          <button
            onClick={() => logout()}
            className="bg-primary text-primary-foreground px-4 py-2 rounded-lg hover:opacity-90 transition"
          >
            Logout
          </button>
        </div>
      </div>
    )
  }

  // Block access if user is rejected
  if (user.status === 'rejected') {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="bg-card border border-border/50 rounded-xl p-8 max-w-md mx-auto text-center">
          <h1 className="text-2xl font-bold text-foreground mb-4">Account Rejected</h1>
          <p className="text-muted mb-4">
            Your account has been rejected. Please contact an administrator if you believe this is an error.
          </p>
          <button
            onClick={() => logout()}
            className="bg-primary text-primary-foreground px-4 py-2 rounded-lg hover:opacity-90 transition"
          >
            Logout
          </button>
        </div>
      </div>
    )
  }

  return <>{children}</>
}
