import {useNavigate} from 'react-router'
import {useForm} from 'react-hook-form'
import {zodResolver} from '@hookform/resolvers/zod'
import {z} from 'zod'
import {PageLayout} from '@/components/layout/page-layout.tsx'
import {Button} from '@/components/ui/button.tsx'
import {Input} from '@/components/ui/input.tsx'
import {Label} from '@/components/ui/label.tsx'
import {useCreateAgentConfigApiAgentConfigsPost} from '@/lib/api/hooks/agent-configs'
import type {AgentCreateRequest} from "@/lib/api";

const agentConfigSchema = z.object({
    prompt: z.string().min(1, 'Prompt is required'),
    agent_name: z.string().optional(),
})

type AgentConfigForm = z.infer<typeof agentConfigSchema>

export function AgentConfigNew() {
    const navigate = useNavigate()
    const createMutation = useCreateAgentConfigApiAgentConfigsPost()

    const {
        register,
        handleSubmit,
        formState: {errors},
    } = useForm<AgentConfigForm>({
        resolver: zodResolver(agentConfigSchema),
        defaultValues: {
            prompt: '',
            agent_name: '',
        },
    })

    const onSubmit = async (data: AgentCreateRequest) => {
        try {
            await createMutation.mutateAsync({data})
            navigate('/agent-configs')
        } catch (error) {
            console.error('Failed to create config:', error)
        }
    }

    return (
        <PageLayout title="New Agent Configuration" description="Create a new AI voice agent configuration">
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
                    <Button type="submit" disabled={createMutation.isPending}>
                        {createMutation.isPending ? 'Creating...' : 'Create Agent'}
                    </Button>
                    <Button type="button" variant="outline" onClick={() => navigate('/agent-configs')}>
                        Cancel
                    </Button>
                </div>
            </form>
        </PageLayout>
    )
}