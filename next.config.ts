import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  ...(process.env.GITHUB_ACTIONS === "true"
    ? {
        output: "export" as const,
        basePath: "/phason-labs",
        assetPrefix: "/phason-labs/",
        trailingSlash: true,
      }
    : {}),
};

export default nextConfig;
