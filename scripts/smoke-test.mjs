import assert from 'node:assert/strict';

const base = process.env.LGPI_TEST_URL ?? 'http://127.0.0.1:3000';
const checks = [
  ['/', ['2024']],
  ['/coverage?year=2023', ['2,981', '2023 financial observations']],
  ['/coverage?year=2024', ['2,987', '2024 financial observations']],
  ['/cities/calgary?year=2023', ['financial year 2023', '2023 transparency score / 33', '2023 source details']],
  ['/cities/calgary?year=2024', ['financial year 2024', '2023 transparency score / 33', '2024 source details']],
  ['/cities/toronto?year=2024', ['Mapping under review', 'change withheld']],
  ['/cities/charlottetown?year=2024', ['Mapping under review', 'change withheld']],
  ['/cities/hamilton?year=2024', ['source unavailable', 'Both years need a reported value']],
  ['/cities/montreal?year=2024', ['2023 transparency score not published']],
  ['/compare', ['Financial year A', 'Financial year B', '2023 transparency components', '2024 source details']],
  ['/metrics', ['?year=2024']],
  ['/methodology', ['2024']],
];
for (const [path, expected] of checks) {
  const response = await fetch(new URL(path, base));
  assert.equal(response.status, 200, path);
  // Ignore embedded hydration payloads so assertions cover visible server-rendered markup.
  const html = (await response.text()).replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, '');
  const text = html.replace(/<!--.*?-->/g, '').replace(/<[^>]*>/g, '');
  for (const fragment of expected) assert.ok((fragment.startsWith('?') ? html : text).includes(fragment), `${path}: missing ${fragment}`);
  if (path.startsWith('/cities/calgary?') || path.startsWith('/coverage?')) {
    const year = new URL(path, base).searchParams.get('year');
    assert.match(html, new RegExp(`aria-current="page"[^>]*>${year}</a>`), `${path}: current year is not announced`);
  }
  console.log(`PASS ${path}`);
}
