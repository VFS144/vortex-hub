import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { Button } from '@/components/ui'

export default function Navbar() {
  const navigate = useNavigate()
  const user = useAuthStore((state) => state.user)
  const logout = useAuthStore((state) => state.logout)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  // Define which roles can access which resources
  const canAccessProjects = user && ['administrator', 'developer'].includes(user.role)
  const canAccessTasks = user && ['administrator', 'developer', 'artist'].includes(user.role)
  const canAccessBugs = user && ['administrator', 'developer', 'game_tester'].includes(user.role)
  const canAccessLore = user && ['administrator', 'lore_writer'].includes(user.role)
  const isAdmin = user?.role === 'administrator'

  const getRoleDisplayName = (role: string) => {
    const roleMap: Record<string, string> = {
      administrator: 'Administrator',
      developer: 'Developer',
      lore_writer: 'Lore Writer',
      artist: 'Artist',
      game_tester: 'Game Tester',
    }
    return roleMap[role] || role
  }

  return (
    <nav className="bg-card border-b border-border/50 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/dashboard" className="flex items-center gap-2 group">
          <img src="/logo.png" alt="Vortex Hub Logo" className="h-8 w-8 object-contain" />
          <span className="text-xl font-bold text-transparent bg-gradient-to-r from-primary to-accent bg-clip-text group-hover:opacity-80 transition">
            Vortex Hub
          </span>
        </Link>

        <div className="flex items-center gap-6">
          {canAccessProjects && (
            <Link to="/projects" className="text-muted hover:text-foreground transition">
              Projects
            </Link>
          )}
          {canAccessTasks && (
            <Link to="/tasks" className="text-muted hover:text-foreground transition">
              Tasks
            </Link>
          )}
          {canAccessBugs && (
            <Link to="/bugs" className="text-muted hover:text-foreground transition">
              Bugs
            </Link>
          )}
          {canAccessLore && (
            <Link to="/lore" className="text-muted hover:text-foreground transition">
              Lore
            </Link>
          )}
          {isAdmin && (
            <Link to="/admin" className="text-muted hover:text-foreground transition font-medium text-accent">
              Admin
            </Link>
          )}
        </div>

        <div className="flex items-center gap-4">
          <div className="text-sm text-muted">
            <span className="text-foreground font-medium">{user?.username}</span>
            {' '}
            <span className="text-primary">({getRoleDisplayName(user?.role || '')})</span>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={handleLogout}
          >
            Logout
          </Button>
        </div>
      </div>
    </nav>
  )
}
