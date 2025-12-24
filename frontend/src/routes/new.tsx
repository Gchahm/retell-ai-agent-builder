import { useNavigate } from 'react-router'
import { PageLayout } from '@/components/layout/page-layout.tsx'
import {
    useCreateAgentConfigApiAgentConfigsPost,
    useGetInitialPromptApiAgentConfigsInitialPromptGet,
} from '@/lib/api/hooks/agent-configs'
import { AgentConfigForm, type AgentConfigFormData } from '@/components/agent-config-form'

export function AgentConfigNew() {
    const navigate = useNavigate()
    const createMutation = useCreateAgentConfigApiAgentConfigsPost()
    const { data: initialPromptData, isPending: isLoadingPrompt } = useGetInitialPromptApiAgentConfigsInitialPromptGet()

    const handleSubmit = async (data: AgentConfigFormData) => {
        try {
            const result = await createMutation.mutateAsync({ data })
            navigate(`/details/${result.agent_id}`)
        } catch (error) {
            console.error('Failed to create config:', error)
        }
    }

    if (isLoadingPrompt) {
        return (
            <PageLayout title="New Agent Configuration" description="Create a new AI voice agent configuration">
                <p>Loading...</p>
            </PageLayout>
        )
    }

    return (
        <PageLayout title="New Agent Configuration" description="Create a new AI voice agent configuration">
            <AgentConfigForm
                mode="create"
                onSubmit={handleSubmit}
                onCancel={() => navigate('/')}
                isSubmitting={createMutation.isPending}
                initialData={{
                    prompt: initialPromptData?.prompt ?? '',
                    agent_name: '',
                }}
            />
        </PageLayout>
    )
}