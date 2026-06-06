import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore, User } from '@/stores/authStore'
import api from '@/lib/api'
import { Button } from '@/components/ui'

interface Stats {
  tasksCount: number
  projectsCount: number
  bugsCount: number
  usersCount: number
  pendingApprovals: number
}

export default function DashboardPage() {
  const navigate = useNavigate()
  const user = useAuthStore((state) => state.user)
  const [stats, setStats] = useState<Stats>({
    tasksCount: 0,
    projectsCount: 0,
    bugsCount: 0,
    usersCount: 0,
    pendingApprovals: 0,
  })
  const [pendingUsers, setPendingUsers] = useState<User[]>([])
  const [isAdminLoading, setIsAdminLoading] = useState(false)
  const [adminError, setAdminError] = useState('')
  const [selectedRoles, setSelectedRoles] = useState<{ [key: number]: string }>({})

  useEffect(() => {
    if (!user) {
      navigate('/login')
      return
    }

    const fetchStats = async () => {
      try {
        // Fetch real-time statistics
        const [tasksRes, projectsRes, bugsRes] = await Promise.all([
          api.get('/api/tasks').catch(() => ({ data: [] })),
          api.get('/api/projects').catch(() => ({ data: [] })),
          api.get('/api/bugs').catch(() => ({ data: [] })),
        ])

        setStats((prev) => ({
          ...prev,
          tasksCount: tasksRes.data.length || 0,
          projectsCount: projectsRes.data.length || 0,
          bugsCount: bugsRes.data.length || 0,
        }))
      } catch (error) {
        console.error('Failed to fetch statistics:', error)
      }
    }

    const fetchPendingUsers = async () => {
      if (user.role !== 'administrator') return

      try {
        setIsAdminLoading(true)
        const response = await api.get('/api/auth/pending')
        setPendingUsers(response.data)
        setStats((prev) => ({
          ...prev,
          pendingApprovals: response.data.length,
        }))
        // Initialize selected roles to game_tester for each user
        const initialRoles: { [key: number]: string } = {}
        response.data.forEach((u: User) => {
          initialRoles[u.id] = 'game_tester'
        })
        setSelectedRoles(initialRoles)
      } catch (error) {
        console.error('Failed to fetch pending users:', error)
        setAdminError('Failed to load pending approvals')
      } finally {
        setIsAdminLoading(false)
      }
    }

    fetchStats()
    fetchPendingUsers()

    // Set up auto-refresh every 30 seconds
    const interval = setInterval(() => {
      fetchStats()
      fetchPendingUsers()
    }, 30000)

    return () => clearInterval(interval)
  }, [user, navigate])

  const handleApproveUser = async (userId: number) => {
    try {
      const role = selectedRoles[userId] || 'game_tester'
      await api.post(`/api/auth/approve/${userId}?assigned_role=${role}`)
      setPendingUsers((prev) => prev.filter((u) => u.id !== userId))
      setStats((prev) => ({
        ...prev,
        pendingApprovals: prev.pendingApprovals - 1,
      }))
    } catch (error) {
      console.error('Failed to approve user:', error)
      setAdminError('Failed to approve user')
    }
  }

  const handleRejectUser = async (userId: number) => {
    try {
      await api.post(`/api/auth/reject/${userId}`)
      setPendingUsers((prev) => prev.filter((u) => u.id !== userId))
      setStats((prev) => ({
        ...prev,
        pendingApprovals: prev.pendingApprovals - 1,
      }))
    } catch (error) {
      console.error('Failed to reject user:', error)
      setAdminError('Failed to reject user')
    }
  }

  if (!user) {
    return null
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">Dashboard</h1>
          <p className="text-muted">Welcome back, {user?.full_name || user?.username}!</p>
        </div>

        {/* Admin Approval Queue - Show at top for administrators */}
        {user.role === 'administrator' && (
          <div className="mb-8">
            <div className="bg-card border border-border/50 rounded-xl p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold text-foreground">
                  Pending Account Approvals
                  {stats.pendingApprovals > 0 && (
                    <span className="ml-2 inline-block bg-destructive text-white px-3 py-1 rounded-full text-sm font-medium">
                      {stats.pendingApprovals}
                    </span>
                  )}
                </h2>
              </div>

              {adminError && (
                <div className="bg-destructive/10 border border-destructive/50 rounded-lg p-4 mb-4 text-destructive">
                  {adminError}
                </div>
              )}

              {isAdminLoading ? (
                <div className="text-center py-8 text-muted">Loading pending approvals...</div>
              ) : pendingUsers.length === 0 ? (
                <div className="text-center py-8 text-muted">No Active Records Found</div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="border-b border-border/50">
                      <tr>
                        <th className="text-left py-3 px-4 text-sm font-semibold text-muted">Username</th>
                        <th className="text-left py-3 px-4 text-sm font-semibold text-muted">Email</th>
                        <th className="text-left py-3 px-4 text-sm font-semibold text-muted">Full Name</th>
                        <th className="text-left py-3 px-4 text-sm font-semibold text-muted">Assign Role</th>
                        <th className="text-left py-3 px-4 text-sm font-semibold text-muted">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {pendingUsers.map((pendingUser) => (
                        <tr key={pendingUser.id} className="border-b border-border/50 hover:bg-card/50 transition">
                          <td className="py-4 px-4 text-sm">{pendingUser.username}</td>
                          <td className="py-4 px-4 text-sm">{pendingUser.email}</td>
                          <td className="py-4 px-4 text-sm">{pendingUser.full_name || '-'}</td>
                          <td className="py-4 px-4 text-sm">
                            <select
                              value={selectedRoles[pendingUser.id] || 'game_tester'}
                              onChange={(e) =>
                                setSelectedRoles((prev) => ({
                                  ...prev,
                                  [pendingUser.id]: e.target.value,
                                }))
                              }
                              className="px-3 py-2 rounded-lg bg-card border border-border text-foreground text-sm"
                            >
                              <option value="administrator">Administrator</option>
                              <option value="developer">Developer</option>
                              <option value="lore_writer">Lore Writer</option>
                              <option value="artist">Artist</option>
                              <option value="game_tester">Game Tester</option>
                            </select>
                          </td>
                          <td className="py-4 px-4 text-sm">
                            <div className="flex gap-2">
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => handleApproveUser(pendingUser.id)}
                                className="text-green-600 border-green-600/30 hover:bg-green-600/10"
                              >
                                Approve
                              </Button>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => handleRejectUser(pendingUser.id)}
                                className="text-red-600 border-red-600/30 hover:bg-red-600/10"
                              >
                                Reject
                              </Button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div className="bg-card border border-border/50 rounded-xl p-6">
            <div className="text-muted text-sm mb-2">Tasks</div>
            <div className="text-3xl font-bold text-primary">{stats.tasksCount}</div>
          </div>
          <div className="bg-card border border-border/50 rounded-xl p-6">
            <div className="text-muted text-sm mb-2">Projects</div>
            <div className="text-3xl font-bold text-primary">{stats.projectsCount}</div>
          </div>
          <div className="bg-card border border-border/50 rounded-xl p-6">
            <div className="text-muted text-sm mb-2">Bugs</div>
            <div className="text-3xl font-bold text-destructive">{stats.bugsCount}</div>
          </div>
          <div className="bg-card border border-border/50 rounded-xl p-6">
            <div className="text-muted text-sm mb-2">Team</div>
            <div className="text-3xl font-bold text-accent">{stats.usersCount}</div>
          </div>
        </div>

        {/* Welcome Message */}
        <div className="bg-gradient-to-r from-primary/10 to-accent/10 border border-primary/30 rounded-xl p-8">
          <h2 className="text-2xl font-bold text-foreground mb-2">Welcome to Vortex Hub</h2>
          <p className="text-muted mb-4">
            The central operating system for Vortex Frame Studios. Your hub for project management, game development tracking, and team collaboration.
          </p>
          <p className="text-primary font-semibold">Every Frame. Infinite Impact.</p>
        </div>
      </div>
    </div>
  )
}
