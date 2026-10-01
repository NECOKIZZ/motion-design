import { chromium } from "/opt/node-tools/node_modules/playwright/index.mjs";
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--ignore-certificate-errors"] });
const ctx = await b.newContext({ ignoreHTTPSErrors: true, viewport: { width: 1440, height: 900 }, colorScheme: "dark" });
const p = await ctx.newPage();
for (const [u, n] of [["https://kickoff.cash/markets", "markets"], ["https://kickoff.cash/", "home"]]) {
  try { await p.goto(u, { waitUntil: "networkidle", timeout: 60000 }); await p.waitForTimeout(2500);
    await p.screenshot({ path: `ref/${n}.png` }); await p.screenshot({ path: `ref/${n}-full.png`, fullPage: true });
    console.log(n, "ok", (await p.content()).length);
  } catch (e) { console.log(n, "fail", e.message); }
}
await b.close();
