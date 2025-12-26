import { useEffect } from 'react'
import { useNavigate, useParams } from 'react-router'
import { useQueryClient } from '@tanstack/react-query'
import { PageLayout } from '@/components/layout/page-layout.tsx'
import { useGetCallApiCallsCallIdGet, listCallsApiCallsGetQueryKey } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { ArrowLeft } from 'lucide-react'
import { CallDetailsCard } from '@/components/call-details-card'
import { TranscriptCard } from '@/components/transcript-card'

export function CallDetails() {
    const navigate = useNavigate()
    const queryClient = useQueryClient()
    const { agentId, callId } = useParams<{ agentId: string; callId: string }>()

    // Invalidate calls list on mount so CallHistory shows updated data
    useEffect(() => {
        queryClient.invalidateQueries({ queryKey: listCallsApiCallsGetQueryKey() })
    }, [queryClient])

    const { data, isPending, error } = useGetCallApiCallsCallIdGet(
        callId!,
        {
            query: {
                enabled: !!callId,
                // Poll every 5 seconds while call status is pending
                refetchInterval: (query) => {
                    const callData = query.state.data
                    if (!callData) return false

                    // Check if status is pending or in-progress
                    const status = callData.status?.toLowerCase()
                    const isPendingStatus = status === 'in-progress';

                    return isPendingStatus ? 5000 : false
                },
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
