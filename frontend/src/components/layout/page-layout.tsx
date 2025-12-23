import type { ReactNode } from "react"

interface PageLayoutProps {
    title: string
    description?: string
    actions?: ReactNode
    children: ReactNode
}

export function PageLayout({ title, description, actions, children }: PageLayoutProps) {
    return (
        <div className="container mx-auto px-4 py-8">
            <div className="mb-8">
                <div className="flex items-center justify-between mb-2">
                    <h1 className="text-3xl font-bold">{title}</h1>
                    {actions && <div className="flex gap-2">{actions}</div>}
                </div>
                {description && <p className="text-muted-foreground">{description}</p>}
            </div>
            {children}
        </div>
    )
}