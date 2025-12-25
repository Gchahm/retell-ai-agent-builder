import {Navigate, Outlet} from 'react-router'
import {useAuth} from '@/lib/auth'

export function ProtectedRoute() {
    const {session, loading} = useAuth()

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-muted-foreground">Loading...</div>
            </div>
        )
    }

    if (!session) {
        return <Navigate to="/login" replace />
    }

    return <Outlet />
}
