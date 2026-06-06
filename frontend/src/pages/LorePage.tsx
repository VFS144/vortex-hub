import { useState, useEffect } from 'react'
import { useAuthStore } from '@/stores/authStore'
import api from '@/lib/api'
import { Button, Card, CardContent, CardHeader, CardTitle, Input, Badge } from '@/components/ui'

interface LoreItem {
  id: number
  name: string
  description?: string
  project_id?: number
  type: 'character' | 'location' | 'faction'
  [key: string]: any
}

interface Project {
  id: number
  name: string
}

export default function LorePage() {
  const user = useAuthStore((state) => state.user)
  const [activeTab, setActiveTab] = useState<'character' | 'location' | 'faction'>('character')
  const [characters, setCharacters] = useState<LoreItem[]>([])
  const [locations, setLocations] = useState<LoreItem[]>([])
  const [factions, setFactions] = useState<LoreItem[]>([])
  const [projects, setProjects] = useState<Project[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [deletingId, setDeletingId] = useState<number | null>(null)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    project_id: '',
  })

  // Check permissions
  const canAccessLore = user && ['administrator', 'lore_writer'].includes(user.role)
  const canCreateLore = canAccessLore

  const loreCategories = [
    {
      title: 'Characters',
      description: 'Create and manage game characters',
      icon: '👤',
      type: 'character' as const,
    },
    {
      title: 'Locations',
      description: 'Define game world locations',
      icon: '🗺️',
      type: 'location' as const,
    },
    {
      title: 'Factions',
      description: 'Organize story factions',
      icon: '⚔️',
      type: 'faction' as const,
    },
  ]

  useEffect(() => {
    if (canAccessLore) {
      fetchAllData()
      // Auto-refresh every 30 seconds
      const interval = setInterval(fetchAllData, 30000)
      return () => clearInterval(interval)
    }
  }, [canAccessLore])

  const fetchAllData = async () => {
    try {
      setIsLoading(true)
      const [charRes, locRes, facRes, projRes] = await Promise.all([
        api.get('/api/lore/characters').catch(() => ({ data: [] })),
        api.get('/api/lore/locations').catch(() => ({ data: [] })),
        api.get('/api/lore/factions').catch(() => ({ data: [] })),
        api.get('/api/projects').catch(() => ({ data: [] })),
      ])
      setCharacters(charRes.data)
      setLocations(locRes.data)
      setFactions(facRes.data)
      setProjects(projRes.data)
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load lore data')
    } finally {
      setIsLoading(false)
    }
  }

  const handleCreateLore = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const endpoint = `/api/lore/${activeTab}s`
      const data = {
        name: formData.name,
        description: formData.description,
        project_id: formData.project_id ? parseInt(formData.project_id) : null,
      }

      const response = await api.post(endpoint, data)

      if (activeTab === 'character') {
        setCharacters([...characters, response.data])
      } else if (activeTab === 'location') {
        setLocations([...locations, response.data])
      } else if (activeTab === 'faction') {
        setFactions([...factions, response.data])
      }

      setFormData({ name: '', description: '', project_id: '' })
      setShowForm(false)
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create lore item')
    }
  }

  const handleDeleteLore = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this item?')) return

    try {
      setDeletingId(id)
      const endpoint = `/api/lore/${activeTab}s/${id}`
      await api.delete(endpoint)

      if (activeTab === 'character') {
        setCharacters(characters.filter((c) => c.id !== id))
      } else if (activeTab === 'location') {
        setLocations(locations.filter((l) => l.id !== id))
      } else if (activeTab === 'faction') {
        setFactions(factions.filter((f) => f.id !== id))
      }
      setError('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete item')
    } finally {
      setDeletingId(null)
    }
  }

  const getLoreItems = () => {
    if (activeTab === 'character') return characters
    if (activeTab === 'location') return locations
    if (activeTab === 'faction') return factions
    return []
  }

  const getProjectName = (projectId?: number) => {
    if (!projectId) return 'No project'
    return projects.find((p) => p.id === projectId)?.name || 'Unknown'
  }

  if (!canAccessLore) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-foreground mb-4">Access Denied</h1>
            <p className="text-muted">Your role does not have access to lore.</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-foreground">Lore Database</h1>
        <p className="text-muted mt-2">Central repository for your game world</p>
      </div>

      {error && (
        <div className="mb-4 bg-destructive/10 border border-destructive/50 rounded-lg p-4 text-destructive">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        {loreCategories.map((category) => (
          <Card
            key={category.title}
            className={`hover:border-primary/50 transition cursor-pointer ${
              activeTab === category.type ? 'border-primary' : ''
            }`}
            onClick={() => setActiveTab(category.type)}
          >
            <CardContent className="p-6 flex flex-col items-center text-center">
              <div className="text-5xl mb-4">{category.icon}</div>
              <h3 className="text-xl font-bold text-foreground mb-2">{category.title}</h3>
              <p className="text-muted text-sm">{category.description}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-foreground capitalize">
            {activeTab.replace(/_/g, ' ')} Entries
          </h2>
          {canCreateLore && (
            <Button onClick={() => setShowForm(!showForm)}>
              {showForm ? 'Cancel' : `New ${activeTab}`}
            </Button>
          )}
        </div>

        {showForm && canCreateLore && (
          <Card className="mb-6">
            <CardContent className="pt-6">
              <form onSubmit={handleCreateLore} className="space-y-4">
                <div>
                  <label className="text-sm font-medium">Name</label>
                  <Input
                    type="text"
                    placeholder={`Enter ${activeTab} name`}
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Description</label>
                  <Input
                    type="text"
                    placeholder={`Describe this ${activeTab}`}
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Link to Project</label>
                  <select
                    className="w-full px-4 py-2 rounded-lg bg-card border border-border text-foreground"
                    value={formData.project_id}
                    onChange={(e) => setFormData({ ...formData, project_id: e.target.value })}
                  >
                    <option value="">No Project</option>
                    {projects.map((p) => (
                      <option key={p.id} value={p.id}>
                        {p.name}
                      </option>
                    ))}
                  </select>
                </div>
                <Button type="submit" className="w-full">
                  Create {activeTab}
                </Button>
              </form>
            </CardContent>
          </Card>
        )}

        {isLoading ? (
          <div className="text-center py-12">
            <div className="text-muted">Loading lore...</div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {getLoreItems().length === 0 ? (
              <div className="col-span-full text-center py-12">
                <div className="text-muted mb-4">No Active Records Found</div>
                {canCreateLore && <Button onClick={() => setShowForm(true)}>Create your first {activeTab}</Button>}
              </div>
            ) : (
              getLoreItems().map((item) => (
                <Card key={item.id} className="hover:border-primary/50 transition">
                  <CardHeader>
                    <CardTitle className="text-lg">{item.name}</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {item.description && (
                      <p className="text-sm text-muted line-clamp-3">{item.description}</p>
                    )}
                    <div>
                      <Badge variant="outline">{getProjectName(item.project_id)}</Badge>
                    </div>
                    {canCreateLore && (
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleDeleteLore(item.id)}
                        disabled={deletingId === item.id}
                        className="w-full"
                      >
                        {deletingId === item.id ? 'Deleting...' : 'Delete'}
                      </Button>
                    )}
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        )}
      </div>

      <Card className="bg-gradient-to-r from-primary/10 to-accent/10 border-primary/30">
        <CardContent className="p-8">
          <h2 className="text-2xl font-bold text-foreground mb-2">Worldbuilding System</h2>
          <p className="text-muted">
            Build a cohesive world for your game with our comprehensive lore management system. Track characters, locations, factions, and more with project linking and organization.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
