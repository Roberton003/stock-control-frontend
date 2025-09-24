// @ts-check
import { test, expect } from '@playwright/test';

// Teste para verificar se a aplicação está acessível
test('should display the main page', async ({ page }) => {
  // Navigate to the main page
  await page.goto('http://localhost:3100');
  
  // Wait for the page to load
  await page.waitForLoadState('networkidle');
  
  // Check if the main content is visible
  const title = page.locator('text=Stock Control Lab');
  await expect(title).toBeVisible();
});

// Teste de login com credenciais válidas
test('should login with valid credentials', async ({ page }) => {
  await page.goto('http://localhost:3100/login');
  
  // Fill in the login form with test credentials
  await page.fill('input[name="username"]', 'admin');
  await page.fill('input[name="password"]', 'admin');
  
  // Submit the form
  await page.click('button[type="submit"]');
  
  // Wait for navigation to dashboard
  await page.waitForURL('http://localhost:3100/dashboard');
  
  // Verify successful login
  const dashboardTitle = page.locator('h1:has-text("Dashboard")');
  await expect(dashboardTitle).toBeVisible();
});

// Teste de listagem de reagentes
test('should display reagents list', async ({ page }) => {
  // First login to get access
  await page.goto('http://localhost:3100/login');
  await page.fill('input[name="username"]', 'admin');
  await page.fill('input[name="password"]', 'admin');
  await page.click('button[type="submit"]');
  await page.waitForURL('http://localhost:3100/dashboard');
  
  // Navigate to reagents page
  await page.goto('http://localhost:3100/reagents');
  await page.waitForLoadState('networkidle');
  
  // Check if reagents are displayed
  const reagentsTable = page.locator('table');
  await expect(reagentsTable).toBeVisible();
});

// Teste de criação de reagente
test('should create a new reagent', async ({ page }) => {
  // First login
  await page.goto('http://localhost:3100/login');
  await page.fill('input[name="username"]', 'admin');
  await page.fill('input[name="password"]', 'admin');
  await page.click('button[type="submit"]');
  await page.waitForURL('http://localhost:3100/dashboard');
  
  // Navigate to reagents page
  await page.goto('http://localhost:3100/reagents');
  
  // Click on add reagent button
  await page.click('button:has-text("Add Reagent")');
  
  // Fill in reagent details
  await page.fill('input#name', 'Test Reagent');
  await page.fill('textarea#description', 'Test reagent description');
  
  // Submit the form
  await page.click('button:has-text("Save")');
  
  // Verify reagent was created
  const successMessage = page.locator('text=Reagent created successfully');
  await expect(successMessage).toBeVisible();
});

// Teste de verificação de dashboard
test('should display dashboard with stats', async ({ page }) => {
  // First login
  await page.goto('http://localhost:3100/login');
  await page.fill('input[name="username"]', 'admin');
  await page.fill('input[name="password"]', 'admin');
  await page.click('button[type="submit"]');
  await page.waitForURL('http://localhost:3100/dashboard');
  
  // Check for dashboard elements
  const lowStockItems = page.locator('text=Low Stock Items');
  const expiringSoon = page.locator('text=Expiring Soon');
  const totalItems = page.locator('text=Total Items');
  
  await expect(lowStockItems).toBeVisible();
  await expect(expiringSoon).toBeVisible();
  await expect(totalItems).toBeVisible();
});

// Teste de navegação entre páginas
test('should navigate between main pages', async ({ page }) => {
  await page.goto('http://localhost:3100');
  
  // Check if navigation links are present
  await expect(page.locator('nav a:has-text("Dashboard")')).toBeVisible();
  await expect(page.locator('nav a:has-text("Reagents")')).toBeVisible();
  await expect(page.locator('nav a:has-text("Stock Lots")')).toBeVisible();
  await expect(page.locator('nav a:has-text("Requisitions")')).toBeVisible();
  
  // Test navigation to each page
  await page.click('nav a:has-text("Dashboard")');
  await expect(page).toHaveURL(/.*dashboard/);
  
  await page.goto('http://localhost:3100');
  await page.click('nav a:has-text("Reagents")');
  await expect(page).toHaveURL(/.*reagents/);
  
  await page.goto('http://localhost:3100');
  await page.click('nav a:has-text("Stock Lots")');
  await expect(page).toHaveURL(/.*stock-lots/);
});