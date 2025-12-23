import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Edit } from 'lucide-react'

interface AgentInfoCardProps {
    name?: string | null
    prompt?: string | null
    agentId: string
    onEdit?: () => void
}

export function AgentInfoCard({ name, prompt, agentId, onEdit }: AgentInfoCardProps) {
    return (
        <Card>
            <CardHeader>
                <div className="flex items-center justify-between">
                    <CardTitle>Agent Information</CardTitle>
                    {onEdit && (
                        <Button variant="outline" size="sm" onClick={onEdit}>
                            <Edit className="mr-2 h-4 w-4" />
                            Edit
                        </Button>
                    )}
                </div>
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
