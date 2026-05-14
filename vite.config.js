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
        proxy: {
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            },
            '/health': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            },
            '/buddy': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            },
            '/identify': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            },
            '/register': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            },
            '/chat': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            },
            '/login': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            },
        },
    },
    preview: {
        host: true,
        port: 5173,
    },
});
