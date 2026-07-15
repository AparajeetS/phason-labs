import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL(process.env.SITE_URL ?? "http://localhost:3000"),
  title: "Phason Labs — Intelligence in Motion",
  description: "An independent AI research lab in Bhubaneswar studying how intelligence reorganizes itself.",
  openGraph: {
    title: "Phason Labs — Intelligence in Motion",
    description: "An independent AI research lab studying how intelligence reorganizes itself.",
    images: [{ url: "/og.png", width: 1734, height: 907, alt: "Phason Labs — Intelligence in Motion" }],
  },
  twitter: { card: "summary_large_image", images: ["/og.png"] },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
