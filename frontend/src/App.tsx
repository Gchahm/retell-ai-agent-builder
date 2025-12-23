import { BrowserRouter, Routes, Route } from 'react-router'
import { Header } from './components/layout/header'
import { Dashboard } from '@/routes'
import { AgentConfigsList } from '@/routes/agent-configs'
import { AgentConfigNew } from './routes/agent-configs/new'


function App() {
    return (
        <BrowserRouter>
            <div className="min-h-screen flex flex-col">
                <Header />
                <main className="flex-1">
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/agent-configs" element={<AgentConfigsList />} />
                        <Route path="/agent-configs/new" element={<AgentConfigNew />} />

                    </Routes>
                </main>
            </div>
        </BrowserRouter>
    )
}

export default App