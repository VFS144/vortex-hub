import { create } from 'zustand';

export type UserRole = 'administrator' | 'developer' | 'lore_writer' | 'artist' | 'game_tester';
export type UserStatus = 'pending' | 'approved' | 'rejected';

export interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  role: UserRole;
  status: UserStatus;
  is_active: boolean;
  created_at: string;
}

interface AuthStore {
  user: User | null;
  isAuthenticated: boolean;
  setUser: (user: User | null) => void;
  logout: () => void;
  isApproved: () => boolean;
  hasRole: (role: UserRole) => boolean;
  canAccessResource: (requiredRole: UserRole[]) => boolean;
}

export const useAuthStore = create<AuthStore>((set, get) => ({
  user: null,
  isAuthenticated: false,
  setUser: (user) => set({ user, isAuthenticated: !!user }),
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    set({ user: null, isAuthenticated: false });
  },
  isApproved: () => {
    const state = get();
    return state.user?.status === 'approved';
  },
  hasRole: (role: UserRole) => {
    const state = get();
    return state.user?.role === role;
  },
  canAccessResource: (requiredRoles: UserRole[]) => {
    const state = get();
    if (!state.user) return false;
    if (state.user.status !== 'approved') return false;
    return requiredRoles.includes(state.user.role);
  },
}));
