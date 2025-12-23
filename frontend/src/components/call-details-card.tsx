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

function renderStructuredDataValue(value: any): string {
    if (value === null || value === undefined) {
        return 'N/A'
    }
    if (typeof value === 'boolean') {
        return value ? 'Yes' : 'No'
    }
    if (typeof value === 'object') {
        return JSON.stringify(value, null, 2)
    }
    return String(value)
}

function formatKey(key: string): string {
    return key
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
}

export function CallDetailsCard({ call }: CallDetailsCardProps) {
    const hasStructuredData = call.structured_data && Object.keys(call.structured_data).length > 0

    return (
        <Card>
            <CardHeader>
                <CardTitle>Call Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
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
                </div>

                {hasStructuredData && (
                    <div className="border-t pt-4">
                        <h3 className="text-sm font-semibold mb-3">Structured Data</h3>
                        <div className="space-y-3">
                            {Object.entries(call.structured_data!).map(([key, value]) => (
                                <div key={key} className="bg-muted rounded-md p-3">
                                    <p className="text-sm font-medium text-muted-foreground mb-1">
                                        {formatKey(key)}
                                    </p>
                                    <div className="text-sm">
                                        {typeof value === 'object' && value !== null ? (
                                            <pre className="whitespace-pre-wrap font-mono text-xs bg-background rounded p-2 overflow-x-auto">
                                                {renderStructuredDataValue(value)}
                                            </pre>
                                        ) : (
                                            <p>{renderStructuredDataValue(value)}</p>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </CardContent>
        </Card>
    )
}
