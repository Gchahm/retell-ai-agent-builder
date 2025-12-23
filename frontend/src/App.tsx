import {BrowserRouter, Route, Routes} from 'react-router'
import {AgentConfigsList} from '@/routes'
import {AgentConfigNew} from './routes/new.tsx'
import {AgentConfigDetails} from './routes/details.tsx'
import {CallDetails} from './routes/call-details.tsx'


function App() {
    return (
        <BrowserRouter>
            <div className="min-h-screen flex flex-col">
                <main className="flex-1">
                    <Routes>
                        <Route path="/" element={<AgentConfigsList />} />
                        <Route path="/new" element={<AgentConfigNew />} />
                        <Route path="/details/:agentId" element={<AgentConfigDetails />} />
                        <Route path="/details/:agentId/calls/:callId" element={<CallDetails />} />
                    </Routes>
                </main>
            </div>
        </BrowserRouter>
    )
}

export default App