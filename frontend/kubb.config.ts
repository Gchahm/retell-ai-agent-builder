import { defineConfig } from '@kubb/core';
import { pluginOas } from '@kubb/plugin-oas';
import { pluginReactQuery } from '@kubb/plugin-react-query';
import { pluginTs } from '@kubb/plugin-ts';
import { pluginZod } from '@kubb/plugin-zod';

export default defineConfig(() => {
  return {
    root: '.',
    input: {
      path: 'http://localhost:8000/openapi.json',
    },
    output: {
      path: './src/lib/api',
      clean: true,
      extension: '',
      format: 'prettier',
    },
    plugins: [
      pluginOas({ validate: false }),
      pluginTs(),
      pluginZod(),
      pluginReactQuery({
        suspense: false,
        group: {
          type: 'tag',
          name: ({ group }) => `${group}`,
        },
      }),
    ],
  };
});
