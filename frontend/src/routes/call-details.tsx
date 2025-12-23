import { useNavigate, useParams } from 'react-router'
import { PageLayout } from '@/components/layout/page-layout.tsx'
import { useGetCallApiCallsCallIdGet } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { ArrowLeft } from 'lucide-react'
import { CallDetailsCard } from '@/components/call-details-card'
import { TranscriptCard } from '@/components/transcript-card'

export function CallDetails() {
    const navigate = useNavigate()
    const { agentId, callId } = useParams<{ agentId: string; callId: string }>()

    const { data, isPending, error } = useGetCallApiCallsCallIdGet(
        callId!,
        {
            query: {
                enabled: !!callId,
            },
        }
    )

    if (isPending) {
        return (
            <PageLayout title="Call Details" description="Loading...">
                <p>Loading call details...</p>
            </PageLayout>
        )
    }

    if (error || !data) {
        return (
            <PageLayout title="Call Details" description="Error loading call">
                <p className="text-destructive">Failed to load call details.</p>
            </PageLayout>
        )
    }

    return (
        <PageLayout
            title="Call Details"
            description="View call information"
        >
            <div className="space-y-6">
                <Button variant="ghost" onClick={() => navigate(`/details/${agentId}`)}>
                    <ArrowLeft className="mr-2 h-4 w-4" />
                    Back to Agent
                </Button>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <CallDetailsCard call={data} />
                    <TranscriptCard transcript={data.transcript} />
                </div>
            </div>
        </PageLayout>
    )
}
