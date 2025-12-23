import { useState } from 'react'
import { useNavigate, useParams, Link } from 'react-router'
import { useQueryClient } from '@tanstack/react-query'
import { PageLayout } from '@/components/layout/page-layout.tsx'
import { useGetAgentConfigApiAgentConfigsAgentIdGet, useUpdateAgentConfigApiAgentConfigsAgentIdPatch } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Edit, ArrowLeft, X } from 'lucide-react'
import { AgentInfoCard } from '@/components/agent-info-card'
import { CallHistory } from '@/components/call-history'
import { TriggerCallForm } from '@/components/trigger-call-form.tsx'
import { AgentConfigForm, type AgentConfigFormData } from '@/components/agent-config-form'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export function AgentConfigDetails() {
    const navigate = useNavigate()
    const { agentId } = useParams<{ agentId: string }>()
    const [isEditing, setIsEditing] = useState(false)
    const queryClient = useQueryClient()
    const updateMutation = useUpdateAgentConfigApiAgentConfigsAgentIdPatch()

    const { data, isPending, error } = useGetAgentConfigApiAgentConfigsAgentIdGet(
        agentId!,
        {
            query: {
                enabled: !!agentId,
            },
        }
    )

    const handleEdit = () => {
        setIsEditing(true)
    }

    const handleCancel = () => {
        setIsEditing(false)
    }

    const handleSubmit = async (formData: AgentConfigFormData) => {
        try {
            await updateMutation.mutateAsync({
                agent_id: agentId!,
                data: {
                    prompt: formData.prompt,
                    agent_name: formData.agent_name || undefined,
                },
            })

            await queryClient.invalidateQueries({
                queryKey: [{ url: `/api/agent-configs/${agentId}` }],
            })

            setIsEditing(false)
        } catch (error) {
            console.error('Failed to update agent config:', error)
            throw error
        }
    }

    if (isPending) {
        return (
            <PageLayout title="Agent Configuration" description="Loading...">
                <p>Loading agent configuration...</p>
            </PageLayout>
        )
    }

    if (error || !data) {
        return (
            <PageLayout title="Agent Configuration" description="Error loading configuration">
                <p className="text-destructive">Failed to load agent configuration.</p>
            </PageLayout>
        )
    }

    return (
        <PageLayout
            title="Agent Configuration Details"
            description="View your AI voice agent configuration"
            actions={
                <div className="flex gap-2">
                    <Button variant="outline" asChild>
                        <Link to={`/edit/${agentId}`}>
                            <Edit className="mr-2 h-4 w-4" />
                            Edit
                        </Link>
                    </Button>
                </div>
            }
        >
            <div className="space-y-6">
                <Button variant="ghost" onClick={() => navigate('/')}>
                    <ArrowLeft className="mr-2 h-4 w-4" />
                    Back to List
                </Button>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {isEditing ? (
                        <Card>
                            <CardHeader>
                                <div className="flex items-center justify-between">
                                    <CardTitle>Edit Agent Information</CardTitle>
                                    <Button
                                        variant="ghost"
                                        size="icon"
                                        onClick={handleCancel}
                                        disabled={updateMutation.isPending}
                                    >
                                        <X className="h-4 w-4" />
                                    </Button>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <AgentConfigForm
                                    initialData={{
                                        prompt: data.prompt || '',
                                        agent_name: data.name || '',
                                    }}
                                    onSubmit={handleSubmit}
                                    onCancel={handleCancel}
                                    isSubmitting={updateMutation.isPending}
                                    mode="edit"
                                />
                            </CardContent>
                        </Card>
                    ) : (
                        <AgentInfoCard
                            name={data.name}
                            prompt={data.prompt}
                            agentId={data.agent_id}
                            onEdit={handleEdit}
                        />
                    )}
                    <div>
                        <TriggerCallForm agentId={data.agent_id}/>
                        <CallHistory agentId={data.agent_id} />
                    </div>
                </div>
            </div>
        </PageLayout>
    )
}
