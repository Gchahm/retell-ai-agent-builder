import { QueryClient } from '@tanstack/react-query'
import fetch from '@kubb/plugin-client/clients/axios';

export interface IClientConfig {
    baseURL: string;
}

export const configureAxios = (config: IClientConfig) => {
    const { baseURL } = config;

    fetch.setConfig({
        baseURL,
    });
};

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