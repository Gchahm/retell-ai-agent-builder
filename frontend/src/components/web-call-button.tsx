import { Button } from '@/components/ui/button'
import { useCreateWebCallApiWebCallsPost } from '@/lib/api'
import { useRetellWebCall } from '@/hooks/useRetellWebCall'
import { Phone, PhoneOff, Loader2, AlertCircle } from 'lucide-react'

interface WebCallButtonProps {
    agentId: string
}

export function WebCallButton({ agentId }: WebCallButtonProps) {
    const { callState, error, startCall, stopCall } = useRetellWebCall()
    const createWebCallMutation = useCreateWebCallApiWebCallsPost()

    const handleCallAction = async () => {
        if (callState === 'active') {
            stopCall()
            return
        }

        try {
            const response = await createWebCallMutation.mutateAsync({
                data: { agent_id: agentId },
            })

            await startCall(response.access_token)
        } catch (err) {
            console.error('Failed to create web call:', err)
        }
    }

    const getButtonConfig = () => {
        switch (callState) {
            case 'idle':
                return {
                    variant: 'default' as const,
                    icon: Phone,
                    text: 'Start Call',
                    disabled: false,
                }
            case 'connecting':
                return {
                    variant: 'default' as const,
                    icon: Loader2,
                    text: 'Connecting...',
                    disabled: true,
                }
            case 'active':
                return {
                    variant: 'destructive' as const,
                    icon: PhoneOff,
                    text: 'End Call',
                    disabled: false,
                }
            case 'error':
                return {
                    variant: 'outline' as const,
                    icon: AlertCircle,
                    text: 'Try Again',
                    disabled: false,
                }
        }
    }

    const config = getButtonConfig()
    const Icon = config.icon

    return (
        <div className="flex flex-col gap-1">
            <Button
                variant={config.variant}
                onClick={handleCallAction}
                disabled={config.disabled}
            >
                <Icon
                    className={`mr-2 h-4 w-4 ${callState === 'connecting' ? 'animate-spin' : ''}`}
                />
                {config.text}
            </Button>
            {callState === 'error' && error && (
                <p className="text-xs text-destructive">{error}</p>
            )}
        </div>
    )
}
