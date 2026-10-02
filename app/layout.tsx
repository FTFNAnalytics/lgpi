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
              <p>Complete 99-municipality source reconstruction built from published LGPI methodology and official municipal records.</p>
            </div>
            <div className="footer-note">
              2023 source pass complete · calculated per-household views remain gated pending exact denominator replication.
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
