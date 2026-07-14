import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geist = Geist({ variable: "--font-geist", subsets: ["latin"] });
const mono = Geist_Mono({ variable: "--font-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  metadataBase: new URL(process.env.SITE_URL ?? "http://localhost:3000"),
  title: "Phason Labs — Intelligence in Motion",
  description: "An independent AI research lab studying world models, machine reasoning, and emergent intelligence.",
  openGraph: {
    title: "Phason Labs — Intelligence in Motion",
    description: "An independent AI research lab studying the hidden structures of intelligence.",
    images: [{ url: "/og.png", width: 1734, height: 907, alt: "Phason Labs — Intelligence in Motion" }],
  },
  twitter: { card: "summary_large_image", images: ["/og.png"] },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body className={`${geist.variable} ${mono.variable}`}>{children}</body></html>;
}
