import { useNavigate } from 'react-router'
import { useListCallsApiCallsGet } from '@/lib/api'
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'

interface CallHistoryProps {
    agentId: string
}

function getStatusVariant(status: string) {
    switch (status.toLowerCase()) {
        case 'completed':
            return 'default'
        case 'failed':
        case 'error':
            return 'destructive'
        default:
            return 'secondary'
    }
}

function formatDate(dateString: string) {
    return new Date(dateString).toLocaleString()
}

export function CallHistory({ agentId }: CallHistoryProps) {
    const navigate = useNavigate()
    const { data: calls, isPending, error } = useListCallsApiCallsGet()

    const agentCalls = calls?.filter(call => call.retell_agent_id === agentId) ?? []

    return (
        <Card>
            <CardHeader>
                <CardTitle>Call History</CardTitle>
            </CardHeader>
            <CardContent>
                {isPending && <p className="text-muted-foreground">Loading calls...</p>}
                {error && <p className="text-destructive">Failed to load calls.</p>}
                {!isPending && !error && agentCalls.length === 0 && (
                    <p className="text-muted-foreground">No calls yet for this agent.</p>
                )}
                {agentCalls.length > 0 && (
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Date</TableHead>
                                <TableHead>Driver</TableHead>
                                <TableHead>Phone</TableHead>
                                <TableHead>Load #</TableHead>
                                <TableHead>Status</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {agentCalls.map(call => (
                                <TableRow
                                    key={call.id}
                                    className="cursor-pointer"
                                    onClick={() => navigate(`/details/${agentId}/calls/${call.id}`)}
                                >
                                    <TableCell>{formatDate(call.created_at)}</TableCell>
                                    <TableCell>{call.driver_name}</TableCell>
                                    <TableCell>{call.phone_number}</TableCell>
                                    <TableCell>{call.load_number}</TableCell>
                                    <TableCell>
                                        <Badge variant={getStatusVariant(call.status)}>
                                            {call.status}
                                        </Badge>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                )}
            </CardContent>
        </Card>
    )
}
