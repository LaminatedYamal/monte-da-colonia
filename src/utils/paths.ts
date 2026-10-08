/**
 * Universal URL helper for Monte da Colónia.
 * Safely handles root domains, custom domains, and GitHub Pages subpaths.
 */
export function url(path: string = ''): string {
  const base = (import.meta.env.BASE_URL || '/').replace(/\/$/, '');
  const clean = path.replace(/^\//, '');
  if (!clean) {
    return base ? `${base}/` : '/';
  }
  return `${base}/${clean}`;
}
