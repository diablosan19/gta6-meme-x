// Courier for the gta6-meme-x-01 entry.
//
// The judged artefact here is a meme post on X, and the only thing this
// program has to do with it is hand the grader its address. It reads the
// address out of POST.json in this repository, makes sure the address
// really points at a single X status, and drops a copy of the record into
// the output folder the grader looks in.
//
// Usage: OUTPUT_DIR=/some/dir node main.ts   (defaults to /output)

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";

const repoRoot = resolve(import.meta.dirname);
const recordFile = join(repoRoot, "POST.json");
const outDir = process.env.OUTPUT_DIR ?? "/output";
const outFile = join(outDir, "POST.json");

function abort(reason: string): never {
  console.error(`[post-courier] ${reason}`);
  process.exit(1);
}

// A valid record is an object whose "url" field is an X status link:
// https://x.com/<handle>/status/<numeric id>, nothing else attached.
function extractStatusUrl(parsed: unknown): string {
  if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
    abort("POST.json does not contain a JSON object");
  }
  const candidate = (parsed as Record<string, unknown>).url;
  if (typeof candidate !== "string") {
    abort('POST.json has no string "url" field');
  }
  let parsedUrl: URL;
  try {
    parsedUrl = new URL(candidate);
  } catch {
    abort(`POST.json url is not a parseable URL: ${candidate}`);
  }
  const segments = parsedUrl.pathname.split("/").filter(Boolean);
  const looksRight =
    parsedUrl.protocol === "https:" &&
    parsedUrl.hostname === "x.com" &&
    segments.length === 3 &&
    segments[1] === "status" &&
    /^[0-9]+$/.test(segments[2]);
  if (!looksRight) {
    abort(`POST.json url is not an X status link: ${candidate}`);
  }
  return candidate;
}

if (!existsSync(recordFile)) {
  abort(`no POST.json found at ${recordFile}`);
}

const rawText = readFileSync(recordFile, "utf8");
let parsed: unknown;
try {
  parsed = JSON.parse(rawText);
} catch {
  abort("POST.json is not valid JSON");
}

const statusUrl = extractStatusUrl(parsed);

mkdirSync(outDir, { recursive: true });
writeFileSync(outFile, rawText, "utf8");
console.log(`[post-courier] wrote ${statusUrl} to ${outFile}`);
