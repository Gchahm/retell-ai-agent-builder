import { useNavigate, useParams, Link } from 'react-router'
import { PageLayout } from '@/components/layout/page-layout.tsx'
import { useGetAgentConfigApiAgentConfigsAgentIdGet } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Edit, ArrowLeft } from 'lucide-react'

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
                    <Button variant="outline" asChild>
                        <Link to={`/edit/${agentId}`}>
                            <Edit className="mr-2 h-4 w-4" />
                            Edit
                        </Link>
                    </Button>
                </div>
            }
        >
            <div className="max-w-2xl space-y-6">
                <Button variant="ghost" onClick={() => navigate('/')}>
                    <ArrowLeft className="mr-2 h-4 w-4" />
                    Back to List
                </Button>

                <div className="space-y-6 border rounded-lg p-6">
                    <div>
                        <h3 className="text-sm font-medium text-muted-foreground mb-2">Agent Name</h3>
                        <p className="text-lg">
                            {data.name || <span className="italic text-muted-foreground">No name set</span>}
                        </p>
                    </div>

                    <div>
                        <h3 className="text-sm font-medium text-muted-foreground mb-2">System Prompt</h3>
                        <div className="bg-muted rounded-md p-4">
                            <pre className="whitespace-pre-wrap font-mono text-sm">
                                {data.agent_id}
                                {data.prompt}
                            </pre>
                        </div>
                    </div>

                    <div>
                        <h3 className="text-sm font-medium text-muted-foreground mb-2">Agent ID</h3>
                        <p className="text-sm font-mono">{data.agent_id}</p>
                    </div>
                </div>
            </div>
        </PageLayout>
    )
}
