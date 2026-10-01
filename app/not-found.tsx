import Link from "next/link";

export default function NotFound() {
  return (
    <main className="section">
      <div className="shell prose">
        <p className="eyebrow">Not found</p>
        <h1>That municipal profile is not loaded yet.</h1>
        <p>A missing profile is not treated as a zero or an absent municipality. It may still be in the reconstruction queue.</p>
        <Link className="button ink" href="/cities">Browse verified profiles</Link>
      </div>
    </main>
  );
}
