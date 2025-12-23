import { useNavigate, useParams, Link } from 'react-router'
import { PageLayout } from '@/components/layout/page-layout.tsx'
import { useGetAgentConfigApiAgentConfigsAgentIdGet } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Edit, ArrowLeft } from 'lucide-react'
import { WebCallButton } from '@/components/web-call-button'
import { AgentInfoCard } from '@/components/agent-info-card'
import { CallHistory } from '@/components/call-history'

export function AgentConfigDetails() {
    const navigate = useNavigate()
    const { agentId } = useParams<{ agentId: string }>()

    const { data, isPending, error } = useGetAgentConfigApiAgentConfigsAgentIdGet(
        agentId!,
        {
            query: {
                enabled: !!agentId,
            },
        }
    )

    if (isPending) {
        return (
            <PageLayout title="Agent Configuration" description="Loading...">
                <p>Loading agent configuration...</p>
            </PageLayout>
        )
    }

    if (error || !data) {
        return (
            <PageLayout title="Agent Configuration" description="Error loading configuration">
                <p className="text-destructive">Failed to load agent configuration.</p>
            </PageLayout>
        )
    }

    return (
        <PageLayout
            title="Agent Configuration Details"
            description="View your AI voice agent configuration"
            actions={
                <div className="flex gap-2">
                    <WebCallButton agentId={agentId!} />
                    <Button variant="outline" asChild>
                        <Link to={`/edit/${agentId}`}>
                            <Edit className="mr-2 h-4 w-4" />
                            Edit
                        </Link>
                    </Button>
                </div>
            }
        >
            <div className="space-y-6">
                <Button variant="ghost" onClick={() => navigate('/')}>
                    <ArrowLeft className="mr-2 h-4 w-4" />
                    Back to List
                </Button>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <AgentInfoCard
                        name={data.name}
                        prompt={data.prompt}
                        agentId={data.agent_id}
                    />
                    <CallHistory agentId={data.agent_id} />
                </div>
            </div>
        </PageLayout>
    )
}
