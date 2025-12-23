import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

const agentConfigSchema = z.object({
    prompt: z.string().min(1, 'Prompt is required'),
    agent_name: z.string().optional(),
})

export type AgentConfigFormData = z.infer<typeof agentConfigSchema>

interface AgentConfigFormProps {
    initialData?: AgentConfigFormData
    onSubmit: (data: AgentConfigFormData) => Promise<void>
    onCancel: () => void
    isSubmitting?: boolean
    mode: 'create' | 'edit'
}

export function AgentConfigForm({
    initialData,
    onSubmit,
    onCancel,
    isSubmitting = false,
    mode,
}: AgentConfigFormProps) {
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<AgentConfigFormData>({
        resolver: zodResolver(agentConfigSchema),
        defaultValues: initialData || {
            prompt: '',
            agent_name: '',
        },
    })

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="max-w-2xl space-y-6">
            <div className="space-y-4">
                <div>
                    <Label htmlFor="agent_name">Agent Name (Optional)</Label>
                    <Input
                        id="agent_name"
                        {...register('agent_name')}
                        placeholder="e.g., Driver Check-In Agent"
                    />
                    {errors.agent_name && (
                        <p className="text-sm text-destructive mt-1">{errors.agent_name.message}</p>
                    )}
                </div>

                <div>
                    <Label htmlFor="prompt">System Prompt</Label>
                    <textarea
                        id="prompt"
                        {...register('prompt')}
                        rows={12}
                        className="w-full border rounded-md p-2"
                        placeholder="You are a logistics dispatcher calling to check on a driver's status..."
                    />
                    {errors.prompt && (
                        <p className="text-sm text-destructive mt-1">{errors.prompt.message}</p>
                    )}
                </div>
            </div>

            <div className="flex gap-2">
                <Button type="submit" disabled={isSubmitting}>
                    {isSubmitting
                        ? mode === 'create'
                            ? 'Creating...'
                            : 'Updating...'
                        : mode === 'create'
                            ? 'Create Agent'
                            : 'Update Agent'}
                </Button>
                <Button type="button" variant="outline" onClick={onCancel}>
                    Cancel
                </Button>
            </div>
        </form>
    )
}
