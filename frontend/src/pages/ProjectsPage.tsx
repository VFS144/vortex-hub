import { useState, useEffect } from 'react'
import { useAuthStore } from '@/stores/authStore'
import api from '@/lib/api'
import { Button, Card, CardContent, CardHeader, CardTitle, Input, Badge } from '@/components/ui'
import { useProjectStore } from '@/stores/projectStore'

export default function ProjectsPage() {
  const user = useAuthStore((state) => state.user)
  const projects = useProjectStore((state) => state.projects)
  const setProjects = useProjectStore((state) => state.setProjects)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({ name: '', description: '', stage: 'concept' })
  const [deletingId, setDeletingId] = useState<number | null>(null)

  // Check permissions
  const canCreateProject = user && ['administrator', 'developer'].includes(user.role)
  const canDeleteProject = user?.role === 'administrator'

  useEffect(() => {
    fetchProjects()
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchProjects, 30000)
    return () => clearInterval(interval)
  }, [])

  const fetchProjects = async () => {
    try {
      setIsLoading(true)
      const response = await api.get('/api/projects')
      setProjects(response.data)
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load projects')
    } finally {
      setIsLoading(false)
    }
  }

  const handleCreateProject = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await api.post('/api/projects', formData)
      setProjects([...projects, response.data])
      setFormData({ name: '', description: '', stage: 'concept' })
      setShowForm(false)
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create project')
    }
  }

  const handleDeleteProject = async (projectId: number) => {
    if (!window.confirm('Are you sure you want to delete this project?')) return

    try {
      setDeletingId(projectId)
      await api.delete(`/api/projects/${projectId}`)
      setProjects(projects.filter((p) => p.id !== projectId))
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete project')
    } finally {
      setDeletingId(null)
    }
  }

  const stageColors = {
    concept: 'secondary',
    prototype: 'default',
    vertical_slice: 'default',
    alpha: 'default',
    beta: 'default',
    release: 'success',
    post_launch: 'success',
  } as const

  if (!user || !['administrator', 'developer', 'game_tester'].includes(user.role)) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-foreground mb-4">Access Denied</h1>
            <p className="text-muted">Your role does not have access to projects.</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold text-foreground">Projects</h1>
          <p className="text-muted mt-2">Manage your game development projects</p>
        </div>
        {canCreateProject && (
          <Button onClick={() => setShowForm(!showForm)}>
            {showForm ? 'Cancel' : 'New Project'}
          </Button>
        )}
      </div>

      {error && (
        <div className="mb-4 bg-destructive/10 border border-destructive/50 rounded-lg p-4 text-destructive">
          {error}
        </div>
      )}

      {showForm && canCreateProject && (
        <Card className="mb-8">
          <CardContent className="pt-6">
            <form onSubmit={handleCreateProject} className="space-y-4">
              <div>
                <label className="text-sm font-medium">Project Name</label>
                <Input
                  type="text"
                  placeholder="Enter project name"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="text-sm font-medium">Description</label>
                <Input
                  type="text"
                  placeholder="Enter project description"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                />
              </div>
              <div>
                <label className="text-sm font-medium">Stage</label>
                <select
                  className="w-full px-4 py-2 rounded-lg bg-card border border-border text-foreground"
                  value={formData.stage}
                  onChange={(e) => setFormData({ ...formData, stage: e.target.value })}
                >
                  <option value="concept">Concept</option>
                  <option value="prototype">Prototype</option>
                  <option value="vertical_slice">Vertical Slice</option>
                  <option value="alpha">Alpha</option>
                  <option value="beta">Beta</option>
                  <option value="release">Release</option>
                  <option value="post_launch">Post Launch</option>
                </select>
              </div>
              <Button type="submit" className="w-full">
                Create Project
              </Button>
            </form>
          </CardContent>
        </Card>
      )}

      {isLoading ? (
        <div className="text-center py-12">
          <div className="text-muted">Loading projects...</div>
        </div>
      ) : projects.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-muted mb-4">No Active Records Found</div>
          {canCreateProject && <Button onClick={() => setShowForm(true)}>Create your first project</Button>}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <Card key={project.id} className="hover:border-primary/50 transition flex flex-col">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <CardTitle className="text-xl">{project.name}</CardTitle>
                  <Badge variant={stageColors[project.stage as keyof typeof stageColors]}>
                    {project.stage.replace(/_/g, ' ')}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4 flex-grow">
                <p className="text-muted text-sm">{project.description}</p>
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm text-muted">Progress</span>
                    <span className="text-sm font-medium">{project.progress}%</span>
                  </div>
                  <div className="w-full h-2 bg-card rounded-full overflow-hidden border border-border/50">
                    <div
                      className="h-full bg-gradient-to-r from-primary to-accent"
                      style={{ width: `${project.progress}%` }}
                    />
                  </div>
                </div>
                {canDeleteProject && (
                  <div className="flex gap-2 mt-4">
                    <Button
                      variant="destructive"
                      size="sm"
                      onClick={() => handleDeleteProject(project.id)}
                      disabled={deletingId === project.id}
                      className="w-full"
                    >
                      {deletingId === project.id ? 'Deleting...' : 'Delete'}
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
