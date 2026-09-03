import type { Metadata } from "next";
import { Manrope, Playfair_Display } from "next/font/google";
import "./globals.css";
const manrope = Manrope({ variable: "--font-manrope", subsets: ["latin"] });
const playfair = Playfair_Display({ variable: "--font-display", subsets: ["latin"] });
export const metadata: Metadata = { title: { default: "Daymark", template: "%s · Daymark" }, description: "A mock todo frontend built to learn Next.js and Django REST integration." };
export default function RootLayout({ children }: LayoutProps<"/">) { return <html lang="en" className={`${manrope.variable} ${playfair.variable}`}><body>{children}</body></html>; }
