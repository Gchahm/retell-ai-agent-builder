import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'
import { useRetellWebCall } from '@/hooks/useRetellWebCall'
import { Phone, PhoneOff, Loader2 } from 'lucide-react'
import { useCreateWebCallApiCallswebcallPost } from '@/lib/api'
import { callCreateSchema } from '@/lib/api/zod/callCreateSchema'

interface TriggerCallFormProps {
    agentId: string
}

const callFormSchema = callCreateSchema.omit({ agent_id: true })

type CallFormData = z.infer<typeof callFormSchema>

export function TriggerCallForm({ agentId }: TriggerCallFormProps) {
    const navigate = useNavigate()
    const [currentCallId, setCurrentCallId] = useState<number | null>(null)
    const prevCallStateRef = useRef<string | null>(null)
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

    useEffect(() => {
        if (prevCallStateRef.current === 'active' && callState === 'idle' && currentCallId) {
            navigate(`/details/${agentId}/calls/${currentCallId}`)
            setCurrentCallId(null)
            reset()
        }
        prevCallStateRef.current = callState
    }, [callState, currentCallId, agentId, navigate, reset])

    const onSubmit = async (data: CallFormData) => {
        try {
            const response = await createWebCallMutation.mutateAsync({
                data: {
                    agent_id: agentId,
                    ...data,
                },
            })

            setCurrentCallId(response.call_id)
            await startCall(response.access_token)
        } catch (err) {
            console.error('Failed to create web call:', err)
        }
    }

    const handleEndCall = () => {
        stopCall()
    }

    const isConnecting = callState === 'connecting'
    const isActive = callState === 'active'

    return (
        <Card>
            <CardHeader>
                <CardTitle>Start Test Call</CardTitle>
            </CardHeader>
            <CardContent>
                <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                    <div>
                        <Label htmlFor="driver_name">Driver Name</Label>
                        <Input
                            id="driver_name"
                            {...register('driver_name')}
                            placeholder="e.g., John Doe"
                            disabled={isConnecting || isActive}
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
                            disabled={isConnecting || isActive}
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
                            disabled={isConnecting || isActive}
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

                    {isActive ? (
                        <Button
                            type="button"
                            variant="destructive"
                            onClick={handleEndCall}
                            className="w-full"
                        >
                            <PhoneOff className="mr-2 h-4 w-4" />
                            End Call
                        </Button>
                    ) : (
                        <Button
                            type="submit"
                            disabled={isConnecting}
                            className="w-full"
                        >
                            {isConnecting ? (
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
                    )}
                </form>
            </CardContent>
        </Card>
    )
}
