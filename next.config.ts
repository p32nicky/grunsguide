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
        // Cloaked cruise affiliate link — Reddit hard-blocks dpbolvw.net directly,
        // but allows vercel.app, so cruise posts link here and redirect through.
        source: "/cruise",
        destination: "https://www.dpbolvw.net/click-1-17037666",
        permanent: false,
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
