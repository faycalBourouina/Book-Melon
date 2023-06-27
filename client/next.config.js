/** @type {import('next').NextConfig} */
module.exports = () => {
    const rewrites = () => {
        return [
          {
            source: '/api/:path*',
            destination: 'http://localhost:8080/:path*' // Proxy to Backend
          }
        ]
    }
    return {
        rewrites,
    }
}
