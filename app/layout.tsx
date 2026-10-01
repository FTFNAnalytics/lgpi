import type { Metadata } from "next";
import { SiteNav } from "@/components/site-nav";
import "./globals.css";

export const metadata: Metadata = {
  title: "LGPI 2023 Reconstruction",
  description: "A source-cited reconstruction of Canada's Local Government Performance Index for 2023.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <SiteNav />
        {children}
        <footer className="site-footer">
          <div className="shell footer-grid">
            <div>
              <strong>LGPI 2023 Reconstruction</strong>
              <p>Independent prototype built from published LGPI methodology and public municipal records.</p>
            </div>
            <div className="footer-note">
              Transparency scores describe financial reporting quality. They are not a fiscal-health rating.
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
