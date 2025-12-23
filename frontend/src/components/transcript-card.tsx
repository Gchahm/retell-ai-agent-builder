import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'

interface TranscriptCardProps {
    transcript?: string | null
}

export function TranscriptCard({ transcript }: TranscriptCardProps) {
    return (
        <Card>
            <CardHeader>
                <CardTitle>Transcript</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="bg-muted rounded-md p-4">
                    {transcript ? (
                        <pre className="whitespace-pre-wrap text-sm">{transcript}</pre>
                    ) : (
                        <p className="text-sm text-muted-foreground italic">No transcript available</p>
                    )}
                </div>
            </CardContent>
        </Card>
    )
}
