import { useState, useEffect } from 'react'
import { useAuthStore } from '@/stores/authStore'
import api from '@/lib/api'
import { Button, Card, CardContent, CardHeader, CardTitle, Input, Badge } from '@/components/ui'
import { useTaskStore } from '@/stores/taskStore'

export default function TasksPage() {
  const user = useAuthStore((state) => state.user)
  const tasks = useTaskStore((state) => state.tasks)
  const setTasks = useTaskStore((state) => state.setTasks)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 'medium',
    status: 'backlog',
  })
  const [editingId, setEditingId] = useState<number | null>(null)
  const [deletingId, setDeletingId] = useState<number | null>(null)
  const [editingStatus, setEditingStatus] = useState<{ [key: number]: string }>({})

  // Check permissions
  const canCreateTask = user && ['administrator', 'developer', 'artist'].includes(user.role)
  const canEditTask = user && ['administrator', 'developer', 'artist'].includes(user.role)
  const canDeleteTask = user && ['administrator', 'developer', 'artist'].includes(user.role)

  useEffect(() => {
    fetchTasks()
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchTasks, 30000)
    return () => clearInterval(interval)
  }, [])

  const fetchTasks = async () => {
    try {
      setIsLoading(true)
      const response = await api.get('/api/tasks')
      setTasks(response.data)
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load tasks')
    } finally {
      setIsLoading(false)
    }
  }

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await api.post('/api/tasks', formData)
      setTasks([...tasks, response.data])
      setFormData({
        title: '',
        description: '',
        priority: 'medium',
        status: 'backlog',
      })
      setShowForm(false)
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create task')
    }
  }

  const handleStatusChange = async (taskId: number, newStatus: string) => {
    try {
      setEditingId(taskId)
      await api.patch(`/api/tasks/${taskId}`, { status: newStatus })
      setTasks(tasks.map((t) => (t.id === taskId ? { ...t, status: newStatus } : t)))
      setEditingStatus({ ...editingStatus, [taskId]: newStatus })
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update task status')
    } finally {
      setEditingId(null)
    }
  }

  const handleDeleteTask = async (taskId: number) => {
    if (!window.confirm('Are you sure you want to delete this task?')) return

    try {
      setDeletingId(taskId)
      await api.delete(`/api/tasks/${taskId}`)
      setTasks(tasks.filter((t) => t.id !== taskId))
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete task')
    } finally {
      setDeletingId(null)
    }
  }

  const priorityColors = {
    low: 'secondary',
    medium: 'default',
    high: 'default',
    critical: 'destructive',
  } as const

  const statusColors = {
    backlog: 'secondary',
    planned: 'default',
    in_progress: 'default',
    testing: 'default',
    blocked: 'destructive',
    done: 'success',
  } as const

  const statuses = ['backlog', 'planned', 'in_progress', 'testing', 'blocked', 'done']

  // Group tasks by status
  const groupedTasks = {
    backlog: tasks.filter((t) => t.status === 'backlog'),
    planned: tasks.filter((t) => t.status === 'planned'),
    in_progress: tasks.filter((t) => t.status === 'in_progress'),
    testing: tasks.filter((t) => t.status === 'testing'),
    blocked: tasks.filter((t) => t.status === 'blocked'),
    done: tasks.filter((t) => t.status === 'done'),
  }

  if (!user || !['administrator', 'developer', 'artist'].includes(user.role)) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-foreground mb-4">Access Denied</h1>
            <p className="text-muted">Your role does not have access to tasks.</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold text-foreground">Tasks</h1>
          <p className="text-muted mt-2">Track your development work</p>
        </div>
        {canCreateTask && (
          <Button onClick={() => setShowForm(!showForm)}>
            {showForm ? 'Cancel' : 'New Task'}
          </Button>
        )}
      </div>

      {error && (
        <div className="mb-4 bg-destructive/10 border border-destructive/50 rounded-lg p-4 text-destructive">
          {error}
        </div>
      )}

      {showForm && canCreateTask && (
        <Card className="mb-8">
          <CardContent className="pt-6">
            <form onSubmit={handleCreateTask} className="space-y-4">
              <div>
                <label className="text-sm font-medium">Task Title</label>
                <Input
                  type="text"
                  placeholder="Enter task title"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  required
                />
              </div>
              <div>
                <label className="text-sm font-medium">Description</label>
                <Input
                  type="text"
                  placeholder="Enter task description"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">Priority</label>
                  <select
                    className="w-full px-4 py-2 rounded-lg bg-card border border-border text-foreground"
                    value={formData.priority}
                    onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="critical">Critical</option>
                  </select>
                </div>
                <div>
                  <label className="text-sm font-medium">Status</label>
                  <select
                    className="w-full px-4 py-2 rounded-lg bg-card border border-border text-foreground"
                    value={formData.status}
                    onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                  >
                    <option value="backlog">Backlog</option>
                    <option value="planned">Planned</option>
                    <option value="in_progress">In Progress</option>
                    <option value="testing">Testing</option>
                    <option value="blocked">Blocked</option>
                    <option value="done">Done</option>
                  </select>
                </div>
              </div>
              <Button type="submit" className="w-full">
                Create Task
              </Button>
            </form>
          </CardContent>
        </Card>
      )}

      {isLoading ? (
        <div className="text-center py-12">
          <div className="text-muted">Loading tasks...</div>
        </div>
      ) : tasks.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-muted mb-4">No Active Records Found</div>
          {canCreateTask && <Button onClick={() => setShowForm(true)}>Create your first task</Button>}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Object.entries(groupedTasks).map(([status, statusTasks]) => (
            <div key={status} className="space-y-4">
              <div className="flex items-center justify-between px-2">
                <h3 className="font-semibold text-foreground capitalize">
                  {status.replace(/_/g, ' ')}
                </h3>
                <span className="text-xs text-muted bg-card px-2 py-1 rounded">
                  {statusTasks.length}
                </span>
              </div>
              <div className="space-y-3">
                {statusTasks.length === 0 ? (
                  <div className="text-center py-8 text-muted text-sm">No Active Records Found</div>
                ) : (
                  statusTasks.map((task) => (
                    <Card key={task.id} className="hover:border-primary/50 transition">
                      <CardContent className="p-4 space-y-3">
                        <div className="font-medium text-foreground">{task.title}</div>
                        {task.description && (
                          <p className="text-sm text-muted line-clamp-2">{task.description}</p>
                        )}
                        <div className="flex gap-2 flex-wrap">
                          <Badge
                            variant={priorityColors[task.priority as keyof typeof priorityColors]}
                            className="text-xs"
                          >
                            {task.priority}
                          </Badge>
                        </div>
                        {canEditTask && (
                          <div className="space-y-2">
                            <label className="text-xs font-medium text-muted">Change Status</label>
                            <select
                              value={editingStatus[task.id] || task.status}
                              onChange={(e) => handleStatusChange(task.id, e.target.value)}
                              disabled={editingId === task.id}
                              className="w-full px-2 py-1.5 text-xs rounded-lg bg-card border border-border text-foreground"
                            >
                              {statuses.map((s) => (
                                <option key={s} value={s}>
                                  {s.replace(/_/g, ' ')}
                                </option>
                              ))}
                            </select>
                          </div>
                        )}
                        {canDeleteTask && (
                          <Button
                            variant="destructive"
                            size="sm"
                            onClick={() => handleDeleteTask(task.id)}
                            disabled={deletingId === task.id}
                            className="w-full"
                          >
                            {deletingId === task.id ? 'Deleting...' : 'Delete'}
                          </Button>
                        )}
                      </CardContent>
                    </Card>
                  ))
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
