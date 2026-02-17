import { defineConfig } from 'vite';

export default defineConfig({
    root: '.',
    build: {
        outDir: 'dist',
        emptyOutDir: true,
        rollupOptions: {
            input: {
                main: './index.html',
            },
        },
    },
    server: {
        host: true,
        port: 5173,
    },
    preview: {
        host: true,
        port: 5173,
    },
});
