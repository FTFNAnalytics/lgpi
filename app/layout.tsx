import type { Metadata } from "next";
import { SiteNav } from "@/components/site-nav";
import "./globals.css";

export const metadata: Metadata = {
  title: "LGPI 2023–2024 Reconstruction",
  description: "A source-cited reconstruction of Canada's Local Government Performance Index with financial data for 2023 and 2024.",
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
              <strong>LGPI 2023–2024 Reconstruction</strong>
              <p>Complete 99-municipality source reconstruction built from published LGPI methodology and official municipal records.</p>
            </div>
            <div className="footer-note">
              2023–2024 financial source passes complete · calculated per-household views remain gated pending exact denominator replication.
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
