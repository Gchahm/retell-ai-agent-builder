import {QueryClient} from '@tanstack/react-query'
import fetch, {axiosInstance} from '@kubb/plugin-client/clients/axios'
import type {AxiosError, InternalAxiosRequestConfig} from 'axios'
import {supabase} from './supabase'

export interface IClientConfig {
    baseURL: string
}

export const configureAxios = (config: IClientConfig) => {
    const {baseURL} = config

    fetch.setConfig({
        baseURL,
    })

    // Add auth token to requests
    axiosInstance.interceptors.request.use(async (config: InternalAxiosRequestConfig) => {
        const {
            data: {session},
        } = await supabase.auth.getSession()
        if (session?.access_token) {
            config.headers.Authorization = `Bearer ${session.access_token}`
        }
        return config
    })

    // Handle 401 responses
    axiosInstance.interceptors.response.use(
        (response) => response,
        async (error: AxiosError) => {
            if (error.response?.status === 401) {
                await supabase.auth.signOut()
                window.location.href = '/login'
            }
            return Promise.reject(error)
        }
    )
}

export const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            staleTime: 1000 * 60 * 5, // 5 minutes
            retry: 1,
            refetchOnWindowFocus: false,
        },
        mutations: {
            retry: 0,
        },
    },
})
