import { Link } from 'react-router'

export function Header() {
    return (
        <header className="border-b">
        <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
        <Link to="/" className="text-xl font-bold">
        AI Voice Agent
    </Link>
    <nav className="flex gap-6">
    <Link to="/agent-configs" className="hover:text-primary">
        Agent Configs
    </Link>
    <Link to="/test-call" className="hover:text-primary">
        Test Call
    </Link>
    <Link to="/results" className="hover:text-primary">
        Results
        </Link>
        </nav>
        </div>
        </div>
        </header>
)
}