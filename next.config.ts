import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async redirects() {
    return [
      {
        // Short, branded affiliate link for YouTube/Reddit/etc — no truncation.
        // Carries the snowball affiliate tag through to gruns.co.
        source: "/vip",
        destination: "https://www.gruns.co/pages/vip?snowball=NICK67621",
        permanent: false, // 302 — keep flexible if the affiliate URL changes
      },
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
      {
        source: "/:path*",
        destination: "https://grunsgummies.site/:path*",
        basePath: false,
        permanent: true, // 301 redirect
        has: [
          {
            type: "host",
            value: "www.grunsgummies.site",
          },
        ],
      },
    ];
  },
};

export default nextConfig;
