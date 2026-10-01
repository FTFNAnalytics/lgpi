import Link from "next/link";

const links = [
  ["Cities", "/cities"],
  ["Transparency", "/transparency"],
  ["Compare", "/compare"],
  ["Metrics", "/metrics"],
  ["Methodology", "/methodology"],
] as const;

export function SiteNav() {
  return (
    <header className="site-header">
      <div className="shell nav-shell">
        <Link href="/" className="brand" aria-label="LGPI home">
          <span className="brand-mark">LGPI</span>
          <span className="brand-copy">Local Government Performance Index</span>
        </Link>
        <nav className="nav-links" aria-label="Primary navigation">
          {links.map(([label, href]) => (
            <Link key={href} href={href}>{label}</Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
