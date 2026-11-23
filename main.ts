// Entry point for the gta6-meme-x-01 submission.
//
// The thing being judged in this competition is not a program at all: it is
// the meme post on X whose address is recorded in POST.json next to this
// file. All this script does is act as the courier for that record. It
// loads POST.json from the repository root, checks that the stored link
// really is an X status URL, and then copies the record into the output
// directory so the grader can pick it up from a predictable place.

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The folder this file lives in is the repository root, which is where
// POST.json sits.
const repoRoot = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(repoRoot, "POST.json");

// The grader expects the record under /output; OUTPUT_DIR lets a human
// point the script at a scratch folder when trying it out locally.
const outputDir = process.env.OUTPUT_DIR ?? "/output";
const targetPath = join(outputDir, "POST.json");

// An X post link: https scheme, x.com host, a handle, the literal word
// "status", and a numeric post id. Anything else means the record is
// broken and there is no point handing it on.
const statusUrlPattern = /^https:\/\/x\.com\/[A-Za-z0-9_]+\/status\/\d+$/;

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

let raw: string;
try {
  raw = readFileSync(sourcePath, "utf8");
} catch {
  fail(`could not read ${sourcePath}`);
}

let record: unknown;
try {
  record = JSON.parse(raw);
} catch {
  fail("POST.json is not valid JSON");
}

const url = (record as { url?: unknown } | null)?.url;
if (typeof url !== "string" || !statusUrlPattern.test(url)) {
  fail("POST.json does not hold an https://x.com/<handle>/status/<id> URL");
}

// Create the output directory when it is missing. It is only ever created
// here, never emptied or removed: whatever else lives in it is not ours
// to touch.
mkdirSync(outputDir, { recursive: true });
writeFileSync(targetPath, raw, "utf8");

console.log(`main.ts: copied the record for ${url} to ${targetPath}`);
