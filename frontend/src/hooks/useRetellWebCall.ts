import { useEffect, useRef, useState, useCallback } from 'react'
import { RetellWebClient } from 'retell-client-js-sdk'

type CallState = 'idle' | 'connecting' | 'active' | 'error'

interface UseRetellWebCallReturn {
    callState: CallState
    error: string | null
    startCall: (accessToken: string) => Promise<void>
    stopCall: () => void
    isCallActive: boolean
}

export function useRetellWebCall(): UseRetellWebCallReturn {
    const retellClientRef = useRef<RetellWebClient | null>(null)
    const [callState, setCallState] = useState<CallState>('idle')
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (!retellClientRef.current) {
            retellClientRef.current = new RetellWebClient()

            retellClientRef.current.on('call_started', () => {
                setCallState('active')
                setError(null)
            })

            retellClientRef.current.on('call_ended', () => {
                setCallState('idle')
                setError(null)
            })

            retellClientRef.current.on('error', (err) => {
                setCallState('error')
                setError(err?.message || 'An error occurred during the call')
            })
        }

        return () => {
            if (retellClientRef.current) {
                try {
                    retellClientRef.current.stopCall()
                } catch (err) {
                    console.error('Cleanup error:', err)
                }
            }
        }
    }, [])

    const startCall = useCallback(async (accessToken: string) => {
        if (!retellClientRef.current) {
            setCallState('error')
            setError('Call client not initialized')
            return
        }

        try {
            setCallState('connecting')
            setError(null)
            await retellClientRef.current.startCall({
                accessToken,
            })
        } catch (err) {
            setCallState('error')
            setError(err instanceof Error ? err.message : 'Failed to start call')
        }
    }, [])

    const stopCall = useCallback(() => {
        if (!retellClientRef.current) {
            return
        }

        try {
            retellClientRef.current.stopCall()
        } catch (err) {
            console.error('Error stopping call:', err)
            setCallState('idle')
        }
    }, [])

    const isCallActive = callState === 'active'

    return {
        callState,
        error,
        startCall,
        stopCall,
        isCallActive,
    }
}
