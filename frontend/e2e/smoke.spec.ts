import { expect, test } from "@playwright/test";

test("dashboard renders and reports backend status", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("heading", { name: /command center|командный центр/i })).toBeVisible();
  await expect(page.getByText(/environment|окружение/i)).toBeVisible();
});

test("backend answers the API metadata endpoint", async ({ request }) => {
  const response = await request.get("/api/v1/meta");

  expect(response.ok()).toBeTruthy();
  const body = (await response.json()) as { all_capabilities: string[] };
  expect(body.all_capabilities).toContain("skills.read");
});
