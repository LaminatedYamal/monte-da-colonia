import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

// https://astro.build/config
// On GitHub Actions CI, deploy with repo subpath; locally run at root /
const isCI = process.env.GITHUB_ACTIONS === 'true';

export default defineConfig({
  site: 'https://laminatedyamal.github.io',
  base: isCI ? '/monte-da-colonia' : '/',
  integrations: [tailwind()],
  server: {
    port: 4321,
    host: true
  }
});
