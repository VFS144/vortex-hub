import { useState, useEffect } from 'react'
import { useAuthStore } from '@/stores/authStore'
import api from '@/lib/api'
import { Button, Card, CardContent, Badge, Input } from '@/components/ui'

interface Bug {
  id: number
  title: string
  description: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  status: 'open' | 'in_progress' | 'complete'
  project_id?: number
  assigned_to?: number
  reported_by: number
  created_at: string
  updated_at: string
}

export default function BugsPage() {
  const user = useAuthStore((state) => state.user)
  const [bugs, setBugs] = useState<Bug[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    severity: 'medium',
  })

  // Check permissions
  const canCreateBug = user && ['administrator', 'developer', 'game_tester'].includes(user.role)
  const canEditBug = user && ['administrator', 'developer'].includes(user.role)
  const canDeleteBug = user?.role === 'administrator'
  const canMarkComplete = user && ['administrator', 'developer'].includes(user.role)

  useEffect(() => {
    fetchBugs()
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchBugs, 30000)
    return () => clearInterval(interval)
  }, [])

  const fetchBugs = async () => {
    try {
      setIsLoading(true)
      const response = await api.get('/api/bugs')
      setBugs(response.data)
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load bugs')
    } finally {
      setIsLoading(false)
    }
  }

  const handleCreateBug = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await api.post('/api/bugs', {
        ...formData,
        status: 'open',
      })
      setBugs([...bugs, response.data])
      setFormData({
        title: '',
        description: '',
        severity: 'medium',
      })
      setShowForm(false)
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create bug')
    }
  }

  const handleUpdateBugStatus = async (bugId: number, newStatus: string) => {
    try {
      const response = await api.patch(`/api/bugs/${bugId}`, {
        status: newStatus,
      })
      setBugs(bugs.map((b) => (b.id === bugId ? response.data : b)))
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update bug')
    }
  }

  const handleDeleteBug = async (bugId: number) => {
    if (!window.confirm('Are you sure you want to delete this bug?')) return

    try {
      await api.delete(`/api/bugs/${bugId}`)
      setBugs(bugs.filter((b) => b.id !== bugId))
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete bug')
    }
  }

  const severityColors = {
    low: 'secondary',
    medium: 'default',
    high: 'default',
    critical: 'destructive',
  } as const

  const statusColors = {
    open: 'default',
    in_progress: 'default',
    complete: 'secondary',
  } as const

  const statusLabels = {
    open: 'Open',
    in_progress: 'In Progress',
    complete: 'Complete',
  } as const

  if (!canCreateBug && user?.role !== 'administrator') {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-foreground mb-4">Access Denied</h1>
            <p className="text-muted">Your role does not have access to bugs.</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold text-foreground">Bug Tracker</h1>
          <p className="text-muted mt-2">Track and manage bugs</p>
        </div>
        {canCreateBug && (
          <Button onClick={() => setShowForm(!showForm)}>
            {showForm ? 'Cancel' : 'Report Bug'}
          </Button>
        )}
      </div>

      {error && (
        <div className="mb-4 bg-destructive/10 border border-destructive/50 rounded-lg p-4 text-destructive">
          {error}
        </div>
      )}

      {showForm && canCreateBug && (
        <Card className="mb-8">
          <CardContent className="pt-6">
            <form onSubmit={handleCreateBug} className="space-y-4">
              <div>
                <label className="text-sm font-medium">Bug Title</label>
                <Input
                  type="text"
                  placeholder="Enter bug title"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="text-sm font-medium">Description</label>
                <Input
                  type="text"
                  placeholder="Enter bug description"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="text-sm font-medium">Severity</label>
                <select
                  className="w-full px-4 py-2 rounded-lg bg-card border border-border text-foreground"
                  value={formData.severity}
                  onChange={(e) => setFormData({ ...formData, severity: e.target.value })}
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="critical">Critical</option>
                </select>
              </div>
              <Button type="submit" className="w-full">
                Report Bug
              </Button>
            </form>
          </CardContent>
        </Card>
      )}

      {isLoading ? (
        <div className="text-center py-12">
          <div className="text-muted">Loading bugs...</div>
        </div>
      ) : bugs.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-muted mb-4">No Active Records Found</div>
          {canCreateBug && <Button onClick={() => setShowForm(true)}>Report your first bug</Button>}
        </div>
      ) : (
        <div className="space-y-3">
          {bugs.map((bug) => (
            <Card key={bug.id} className="hover:border-destructive/50 transition">
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-medium text-foreground mb-2">{bug.title}</h3>
                    <p className="text-sm text-muted mb-3">{bug.description}</p>
                    <div className="flex gap-2 flex-wrap">
                      <Badge variant={severityColors[bug.severity]}>
                        {bug.severity.charAt(0).toUpperCase() + bug.severity.slice(1)}
                      </Badge>
                      <Badge variant={statusColors[bug.status]}>
                        {statusLabels[bug.status]}
                      </Badge>
                    </div>
                  </div>
                  <div className="ml-4 flex flex-col gap-2">
                    {canMarkComplete && bug.status === 'open' && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleUpdateBugStatus(bug.id, 'in_progress')}
                      >
                        Start Work
                      </Button>
                    )}
                    {canMarkComplete && bug.status === 'in_progress' && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleUpdateBugStatus(bug.id, 'complete')}
                        className="text-green-600 border-green-600/30"
                      >
                        Mark Complete
                      </Button>
                    )}
                    {canDeleteBug && bug.status === 'complete' && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleDeleteBug(bug.id)}
                        className="text-red-600 border-red-600/30"
                      >
                        Delete
                      </Button>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
