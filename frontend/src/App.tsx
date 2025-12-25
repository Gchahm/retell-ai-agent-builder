import {BrowserRouter, Route, Routes} from 'react-router'
import {AuthProvider} from '@/lib/auth'
import {ProtectedRoute} from '@/components/protected-route'
import {AgentConfigsList} from '@/routes'
import {AgentConfigNew} from './routes/new.tsx'
import {AgentConfigDetails} from './routes/details.tsx'
import {CallDetails} from './routes/call-details.tsx'
import {LoginPage} from './routes/login.tsx'

function AppRoutes() {
    return (
        <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route element={<ProtectedRoute />}>
                <Route path="/" element={<AgentConfigsList />} />
                <Route path="/new" element={<AgentConfigNew />} />
                <Route path="/details/:agentId" element={<AgentConfigDetails />} />
                <Route path="/details/:agentId/calls/:callId" element={<CallDetails />} />
            </Route>
        </Routes>
    )
}

function App() {
    return (
        <BrowserRouter>
            <AuthProvider>
                <div className="min-h-screen flex flex-col">
                    <main className="flex-1">
                        <AppRoutes />
                    </main>
                </div>
            </AuthProvider>
        </BrowserRouter>
    )
}

export default App
