/** @type {import('next').NextConfig} */
const nextConfig = {}

module.exports = {
    reactStrictMode: false,
    webpack5: true,
    webpack: (config) => {
        config.resolve.fallback = {
            fs: false,
            async_hooks: false
        };

        return config;
    }
}
