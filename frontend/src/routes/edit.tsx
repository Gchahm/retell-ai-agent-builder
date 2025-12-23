import { useNavigate, useParams } from 'react-router'
import { PageLayout } from '@/components/layout/page-layout.tsx'
import {
    useGetAgentConfigApiAgentConfigsAgentIdGet,
    useUpdateAgentConfigApiAgentConfigsAgentIdPatch,
} from '@/lib/api/hooks/index'
import { AgentConfigForm, type AgentConfigFormData } from '@/components/agent-config-form'

export function AgentConfigEdit() {
    const navigate = useNavigate()
    const { agentId } = useParams<{ agentId: string }>()

    const { data: agentConfig, isLoading, error } = useGetAgentConfigApiAgentConfigsAgentIdGet(
        agentId!,
        {
            query: {
                enabled: !!agentId,
            },
        }
    )

    const updateMutation = useUpdateAgentConfigApiAgentConfigsAgentIdPatch()

    const handleSubmit = async (data: AgentConfigFormData) => {
        if (!agentId) return

        try {
            await updateMutation.mutateAsync({
                agent_id: agentId,
                data,
            })
            navigate('/agent-configs')
        } catch (error) {
            console.error('Failed to update config:', error)
        }
    }

    if (isLoading) {
        return (
            <PageLayout title="Edit Agent Configuration" description="Loading...">
                <p>Loading agent configuration...</p>
            </PageLayout>
        )
    }

    if (error || !agentConfig) {
        return (
            <PageLayout title="Edit Agent Configuration" description="Error loading configuration">
                <p className="text-destructive">Failed to load agent configuration.</p>
            </PageLayout>
        )
    }

    // Extract prompt from response_engine
    const getPrompt = () => {
        const engine = agentConfig.response_engine
        if ('general_prompt' in engine) {
            return engine.general_prompt
        }
        if ('begin_message' in engine) {
            return engine.begin_message || ''
        }
        return ''
    }

    const initialData: AgentConfigFormData = {
        prompt: getPrompt(),
        agent_name: agentConfig.agent_name || '',
    }

    return (
        <PageLayout
            title="Edit Agent Configuration"
            description="Update your AI voice agent configuration"
        >
            <AgentConfigForm
                mode="edit"
                initialData={initialData}
                onSubmit={handleSubmit}
                onCancel={() => navigate('/')}
                isSubmitting={updateMutation.isPending}
            />
        </PageLayout>
    )
}
