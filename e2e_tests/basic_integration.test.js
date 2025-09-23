// @ts-check
const { test, expect } = require('@playwright/test');

test('should display reagents list', async ({ page }) => {
  // Navigate to the reagents page
  await page.goto('http://localhost:3000');
  
  // Wait for the page to load
  await page.waitForLoadState('networkidle');
  
  // Check if the reagents list is displayed
  const reagentsHeader = page.locator('h1:has-text("Reagents")');
  await expect(reagentsHeader).toBeVisible();
});

test('should login and display dashboard', async ({ page }) => {
  // Navigate to the login page
  await page.goto('http://localhost:3000/login');
  
  // Fill in the login form
  await page.fill('input[name="username"]', 'admin');
  await page.fill('input[name="password"]', 'admin');
  
  // Submit the form
  await page.click('button[type="submit"]');
  
  // Wait for navigation
  await page.waitForURL('http://localhost:3000/dashboard');
  
  // Check if the dashboard is displayed
  const dashboardHeader = page.locator('h1:has-text("Dashboard")');
  await expect(dashboardHeader).toBeVisible();
});