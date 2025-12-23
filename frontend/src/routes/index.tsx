import {Link} from 'react-router'
import {PageLayout} from '@/components/layout/page-layout.tsx'
import {Button} from '@/components/ui/button.tsx'
import {Plus} from 'lucide-react'
import {useListAgentConfigsApiAgentConfigsGet} from '@/lib/api/hooks/agent-configs'
import type {AgentResponse} from "@/lib/api";

export function AgentConfigsList() {
    const { data, isPending, error } = useListAgentConfigsApiAgentConfigsGet()

    if (isPending) return <div>Loading...</div>
    if (error) return <div>Error: {error.message}</div>

    return (
        <PageLayout
            title="Agent Configurations"
            description="Manage your AI voice agent configurations"
            actions={
                <Button asChild>
                    <Link to="/new">
                        <Plus className="mr-2 h-4 w-4" />
                        New Configuration
                    </Link>
                </Button>
            }
        >
            {data.length === 0 ? (
                <div className="text-center py-12">
                    <p className="text-muted-foreground mb-4">No agent configurations yet</p>
                    <Button asChild>
                        <Link to="/new">Create your first configuration</Link>
                    </Button>
                </div>
            ) : (
                <div className="border rounded-lg">
                    <table className="w-full">
                        <thead className="border-b bg-muted/50">
                        <tr>
                            <th className="text-left p-4 font-medium">Name</th>
                        </tr>
                        </thead>
                        <tbody>
                        {data.map((config: AgentResponse) => (
                            <tr key={config.agent_id} className="border-b last:border-0 hover:bg-muted/50">
                                <td className="p-4 font-medium">
                                    <Link to={`/details/${config.agent_id}`} className="hover:underline">
                                        {config.agent_name || 'Unnamed Agent'}
                                    </Link>
                                </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            )}
        </PageLayout>
    )
}