/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    CLOUD_NAME: process.env.CLOUD_NAME,
    API_KEY: process.env.API_KEY,
    API_SECRET: process.env.API_SECRET,
  },
  rewrites: async () => {
    return [
      {
        source: "/api/:path*",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:5328/api/:path*"
            : "/api/",
      },
    ];
  },
};

module.exports = nextConfig
