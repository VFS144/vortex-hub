import { create } from 'zustand';

export interface Project {
  id: number;
  name: string;
  description?: string;
  stage: string;
  budget?: string;
  progress: number;
  lead_id?: number;
}

interface ProjectStore {
  projects: Project[];
  currentProject: Project | null;
  setProjects: (projects: Project[]) => void;
  setCurrentProject: (project: Project | null) => void;
  addProject: (project: Project) => void;
  updateProject: (id: number, project: Partial<Project>) => void;
}

export const useProjectStore = create<ProjectStore>((set) => ({
  projects: [],
  currentProject: null,
  setProjects: (projects) => set({ projects }),
  setCurrentProject: (project) => set({ currentProject: project }),
  addProject: (project) => set((state) => ({ projects: [...state.projects, project] })),
  updateProject: (id, project) =>
    set((state) => ({
      projects: state.projects.map((p) => (p.id === id ? { ...p, ...project } : p)),
    })),
}));
