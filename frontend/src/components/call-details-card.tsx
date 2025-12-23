import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import type { CallResponse } from '@/lib/api/types/CallResponse'

interface CallDetailsCardProps {
    call: CallResponse
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

export function CallDetailsCard({ call }: CallDetailsCardProps) {
    return (
        <Card>
            <CardHeader>
                <CardTitle>Call Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <p className="text-sm font-medium text-muted-foreground">Driver Name</p>
                        <p className="text-sm">{call.driver_name}</p>
                    </div>
                    <div>
                        <p className="text-sm font-medium text-muted-foreground">Phone Number</p>
                        <p className="text-sm">{call.phone_number}</p>
                    </div>
                    <div>
                        <p className="text-sm font-medium text-muted-foreground">Load Number</p>
                        <p className="text-sm">{call.load_number}</p>
                    </div>
                    <div>
                        <p className="text-sm font-medium text-muted-foreground">Status</p>
                        <Badge variant={getStatusVariant(call.status)}>
                            {call.status}
                        </Badge>
                    </div>
                    <div>
                        <p className="text-sm font-medium text-muted-foreground">Created At</p>
                        <p className="text-sm">{formatDate(call.created_at)}</p>
                    </div>
                    <div>
                        <p className="text-sm font-medium text-muted-foreground">Updated At</p>
                        <p className="text-sm">{formatDate(call.updated_at)}</p>
                    </div>
                    {call.retell_call_id && (
                        <div className="col-span-2">
                            <p className="text-sm font-medium text-muted-foreground">Retell Call ID</p>
                            <p className="text-sm font-mono">{call.retell_call_id}</p>
                        </div>
                    )}
                </div>
            </CardContent>
        </Card>
    )
}
