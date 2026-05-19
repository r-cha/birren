#!/usr/bin/env node
const path = require('path');
const { chromium } = require('playwright');

const HERE = __dirname;
const REPO = path.resolve(HERE, '..');
const SOURCE = path.join(HERE, 'og-image.html');
const OUTPUT = path.join(REPO, 'og-image.png');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1200, height: 630 },
    deviceScaleFactor: 2,
  });
  const page = await context.newPage();
  await page.goto('file://' + SOURCE, { waitUntil: 'load' });
  await page.waitForLoadState('networkidle');
  await page.screenshot({
    path: OUTPUT,
    clip: { x: 0, y: 0, width: 1200, height: 630 },
    omitBackground: false,
    type: 'png',
  });
  await browser.close();
  console.log('wrote', OUTPUT);
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
