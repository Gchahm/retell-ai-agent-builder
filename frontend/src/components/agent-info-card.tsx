import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'

interface AgentInfoCardProps {
    name?: string | null
    prompt?: string | null
    agentId: string
}

export function AgentInfoCard({ name, prompt, agentId }: AgentInfoCardProps) {
    return (
        <Card>
            <CardHeader>
                <CardTitle>Agent Information</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
                <div>
                    <h3 className="text-sm font-medium text-muted-foreground mb-2">Agent Name</h3>
                    <p className="text-lg">
                        {name || <span className="italic text-muted-foreground">No name set</span>}
                    </p>
                </div>

                <div>
                    <h3 className="text-sm font-medium text-muted-foreground mb-2">System Prompt</h3>
                    <div className="bg-muted rounded-md p-4">
                        <pre className="whitespace-pre-wrap font-mono text-sm">
                            {prompt}
                        </pre>
                    </div>
                </div>

                <div>
                    <h3 className="text-sm font-medium text-muted-foreground mb-2">Agent ID</h3>
                    <p className="text-sm font-mono">{agentId}</p>
                </div>
            </CardContent>
        </Card>
    )
}
