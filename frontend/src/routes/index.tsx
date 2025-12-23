import {Link} from 'react-router'
import {PageLayout} from '@/components/layout/page-layout'
import {Settings, Phone, FileText} from 'lucide-react'

export function Dashboard() {
    return (
        <PageLayout
            title="AI Voice Agent Dashboard"
            description="Configure agents, trigger test calls, and review results"
        >
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <DashboardCard
                    title="Agent Configurations"
                    description="Create and manage AI voice agent configurations"
                    icon={<Settings className="h-8 w-8"/>}
                    href="/agent-configs"
                />
                <DashboardCard
                    title="Test Call"
                    description="Trigger a test call to a driver"
                    icon={<Phone className="h-8 w-8"/>}
                    href="/test-call"
                />
                <DashboardCard
                    title="Call Results"
                    description="View call transcripts and structured data"
                    icon={<FileText className="h-8 w-8"/>}
                    href="/results"
                />
            </div>
        </PageLayout>
    )
}

function DashboardCard({
                           title,
                           description,
                           icon,
                           href,
                       }: {
    title: string
    description: string
    icon: React.ReactNode
    href: string
}) {
    return (
        <Link to={href}>
            <div className="border rounded-lg p-6 hover:border-primary transition-colors cursor-pointer">
                <div className="mb-4 text-primary">{icon}</div>
                <h3 className="text-xl font-semibold mb-2">{title}</h3>
                <p className="text-muted-foreground text-sm">{description}</p>
            </div>
        </Link>
    )
}