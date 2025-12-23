import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useRetellWebCall } from '@/hooks/useRetellWebCall'
import { Phone, PhoneOff, Loader2, AlertCircle, X } from 'lucide-react'
import { useCreateWebCallApiCallswebcallPost } from '@/lib/api'
import type { CallCreate } from '@/lib/api/types/CallCreate'

interface WebCallButtonProps {
    agentId: string
}

const callFormSchema = z.object({
    driver_name: z.string().min(1, 'Driver name is required'),
    phone_number: z.string().min(1, 'Phone number is required'),
    load_number: z.string().min(1, 'Load number is required'),
})

type CallFormData = z.infer<typeof callFormSchema>

export function WebCallButton({ agentId }: WebCallButtonProps) {
    const [showForm, setShowForm] = useState(false)
    const { callState, error, startCall, stopCall } = useRetellWebCall()
    const createWebCallMutation = useCreateWebCallApiCallswebcallPost()

    const {
        register,
        handleSubmit,
        formState: { errors },
        reset,
    } = useForm<CallFormData>({
        resolver: zodResolver(callFormSchema),
        defaultValues: {
            driver_name: '',
            phone_number: '',
            load_number: '',
        },
    })

    const handleCallAction = () => {
        if (callState === 'active') {
            stopCall()
            setShowForm(false)
            reset()
        } else if (callState === 'idle' || callState === 'error') {
            setShowForm(true)
        }
    }

    const onSubmit = async (data: CallFormData) => {
        try {
            const callData: CallCreate = {
                retell_agent_id: agentId,
                driver_name: data.driver_name,
                phone_number: data.phone_number,
                load_number: data.load_number,
            }

            const response = await createWebCallMutation.mutateAsync({
                data: callData,
            })

            await startCall(response.access_token)
        } catch (err) {
            console.error('Failed to create web call:', err)
        }
    }

    const handleCancel = () => {
        setShowForm(false)
        reset()
    }

    if (showForm && callState !== 'active') {
        return (
            <div className="border rounded-lg p-4 space-y-4 bg-background">
                <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold">Start Call</h3>
                    <Button
                        variant="ghost"
                        size="icon"
                        onClick={handleCancel}
                        disabled={callState === 'connecting'}
                    >
                        <X className="h-4 w-4" />
                    </Button>
                </div>

                <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                    <div>
                        <Label htmlFor="driver_name">Driver Name</Label>
                        <Input
                            id="driver_name"
                            {...register('driver_name')}
                            placeholder="e.g., John Doe"
                            disabled={callState === 'connecting'}
                        />
                        {errors.driver_name && (
                            <p className="text-sm text-destructive mt-1">
                                {errors.driver_name.message}
                            </p>
                        )}
                    </div>

                    <div>
                        <Label htmlFor="phone_number">Phone Number</Label>
                        <Input
                            id="phone_number"
                            {...register('phone_number')}
                            placeholder="e.g., +1234567890"
                            disabled={callState === 'connecting'}
                        />
                        {errors.phone_number && (
                            <p className="text-sm text-destructive mt-1">
                                {errors.phone_number.message}
                            </p>
                        )}
                    </div>

                    <div>
                        <Label htmlFor="load_number">Load Number</Label>
                        <Input
                            id="load_number"
                            {...register('load_number')}
                            placeholder="e.g., LD-12345"
                            disabled={callState === 'connecting'}
                        />
                        {errors.load_number && (
                            <p className="text-sm text-destructive mt-1">
                                {errors.load_number.message}
                            </p>
                        )}
                    </div>

                    {callState === 'error' && error && (
                        <div className="bg-destructive/10 border border-destructive rounded-md p-3">
                            <p className="text-sm text-destructive">{error}</p>
                        </div>
                    )}

                    <div className="flex gap-2">
                        <Button
                            type="submit"
                            disabled={callState === 'connecting'}
                            className="flex-1"
                        >
                            {callState === 'connecting' ? (
                                <>
                                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                    Connecting...
                                </>
                            ) : (
                                <>
                                    <Phone className="mr-2 h-4 w-4" />
                                    Start Call
                                </>
                            )}
                        </Button>
                        <Button
                            type="button"
                            variant="outline"
                            onClick={handleCancel}
                            disabled={callState === 'connecting'}
                        >
                            Cancel
                        </Button>
                    </div>
                </form>
            </div>
        )
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
            {callState === 'error' && error && !showForm && (
                <p className="text-xs text-destructive">{error}</p>
            )}
        </div>
    )
}
