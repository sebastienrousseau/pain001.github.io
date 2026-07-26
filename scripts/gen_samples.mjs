/* Write the demo's sample batches as downloadable CSV files.
 *
 * Single source of truth: static/js/try-demo.js exports SAMPLES; this
 * script materialises them under <outdir>/ at build time so the files
 * users download are byte-identical to what "Load a sample" loads.
 *
 * Usage: node scripts/gen_samples.mjs <outdir>
 */

import { mkdir, writeFile } from "node:fs/promises";
import { SAMPLES } from "../static/js/try-demo.js";

const outdir = process.argv[2];
if (!outdir) {
  console.error("usage: gen_samples.mjs <outdir>");
  process.exit(1);
}

await mkdir(outdir, { recursive: true });
for (const [key, sample] of Object.entries(SAMPLES)) {
  const path = `${outdir}/pain001-sample-${key}.csv`;
  await writeFile(path, sample.csv.trim() + "\n", "utf-8");
  console.log(`[samples] wrote ${path}`);
}
