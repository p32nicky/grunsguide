import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async redirects() {
    return [
      {
        source: "/:path*",
        destination: "https://grunsgummies.site/:path*",
        basePath: false,
        permanent: true, // 301 redirect
        has: [
          {
            type: "host",
            value: "grunsguide.vercel.app",
          },
        ],
      },
    ];
  },
};

export default nextConfig;
