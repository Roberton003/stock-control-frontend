import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e_tests',
  timeout: 30000,
  expect: {
    timeout: 5000
  },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 1,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    actionTimeout: 0,
    baseURL: 'http://localhost:3100',  // Atualizado para refletir a porta do frontend no Docker
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { channel: 'chrome' },
    },
  ],
  webServer: {
    command: 'npm run dev',
    port: 3100,  // Atualizado para refletir a porta do frontend no Docker
    timeout: 120000,
    reuseExistingServer: !process.env.CI,
  },
});