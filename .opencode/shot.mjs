import { chromium } from "playwright";

const label = process.argv[2] ?? "before";
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 375, height: 800 } });
await page.goto("http://localhost:8080/");
await page.fill("#source", "hallucinate(“the slop must flow”)✨");
await page.click("#run");
await page.waitForFunction(
  () => document.getElementById("output").textContent !== "Running…",
);
const narrow = await page.evaluate(() => ({
  scrollWidth: document.documentElement.scrollWidth,
  clientWidth: document.documentElement.clientWidth,
  outputWidth: document.getElementById("output").getBoundingClientRect().width,
  text: document.getElementById("output").textContent,
}));
await page.screenshot({ path: `.opencode/${label}-375.png`, fullPage: true });

await page.setViewportSize({ width: 1280, height: 900 });
const wide = await page.evaluate(() => ({
  scrollWidth: document.documentElement.scrollWidth,
  clientWidth: document.documentElement.clientWidth,
  outputWidth: document.getElementById("output").getBoundingClientRect().width,
}));
await page.screenshot({ path: `.opencode/${label}-1280.png`, fullPage: true });

console.log(JSON.stringify({ narrow, wide }, null, 2));
await browser.close();
