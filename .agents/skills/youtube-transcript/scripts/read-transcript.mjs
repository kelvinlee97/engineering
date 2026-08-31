import { readFile as readTextFile } from "node:fs/promises";

const EXPAND_SELECTOR = "#description-inline-expander #expand";
const SHOW_TRANSCRIPT_SELECTOR = "ytd-video-description-transcript-section-renderer button";
const TRANSCRIPT_SEGMENTS_SELECTOR =
  'ytd-engagement-panel-section-list-renderer[target-id="engagement-panel-searchable-transcript"]' +
  '[visibility="ENGAGEMENT_PANEL_VISIBILITY_EXPANDED"] ytd-transcript-segment-renderer';

function isTransient(error) {
  const message = String(error?.message ?? error).toLowerCase();
  return (
    message.includes("not attached") ||
    message.includes("no_matches") ||
    message.includes("selector deadline")
  );
}

function extractSegments(elements) {
  return elements.map((element) => {
    const timestamp = element.querySelector(".segment-timestamp")?.textContent?.trim();
    const text = element.querySelector(".segment-text")?.textContent?.replace(/\s+/g, " ").trim();
    if (!timestamp || !text) throw new Error("Malformed transcript segment");
    const parts = timestamp.split(":").map(Number);
    if (
      parts.length < 2 ||
      parts.length > 3 ||
      parts.some((part) => !Number.isFinite(part) || part < 0)
    ) {
      throw new Error("Malformed transcript timestamp");
    }
    const start_seconds =
      parts.length === 3 ? parts[0] * 3600 + parts[1] * 60 + parts[2] : parts[0] * 60 + parts[1];
    return { start_seconds, text };
  });
}

function validateSegments(segments) {
  if (!Array.isArray(segments) || segments.length === 0) {
    throw new Error("Transcript read returned no segments");
  }
  for (let index = 0; index < segments.length; index += 1) {
    const segment = segments[index];
    if (
      !Number.isFinite(segment?.start_seconds) ||
      segment.start_seconds < 0 ||
      typeof segment.text !== "string" ||
      !segment.text.trim()
    ) {
      throw new Error(`Transcript segment ${index + 1} is invalid`);
    }
    if (index > 0 && segment.start_seconds < segments[index - 1].start_seconds) {
      throw new Error(`Transcript timestamps move backwards at segment ${index + 1}`);
    }
  }
}

function parseHelperExport(rawExport) {
  const segments = [];
  for (const line of rawExport.split(/\r?\n/)) {
    if (!line.startsWith("[")) continue;
    const match = line.match(/^\[([0-9]+(?::[0-9]{2}){1,2})\]\s+(.+)$/);
    if (!match) throw new Error("Malformed helper transcript line");
    const parts = match[1].split(":").map(Number);
    const start_seconds =
      parts.length === 3 ? parts[0] * 3600 + parts[1] * 60 + parts[2] : parts[0] * 60 + parts[1];
    segments.push({ start_seconds, text: match[2].replace(/\s+/g, " ").trim() });
  }
  validateSegments(segments);
  return segments;
}

export async function readYouTubeTranscript(
  tab,
  {
    now = Date.now,
    pollIntervalMs = 250,
    readFile = readTextFile,
    timeoutMs = 10_000,
  } = {},
) {
  const startedAt = now();
  let descriptionExpanded = false;
  let transcriptOpened = false;

  while (now() - startedAt < timeoutMs) {
    const transcriptSegments = tab.playwright.locator(TRANSCRIPT_SEGMENTS_SELECTOR);
    if ((await transcriptSegments.count()) > 0) {
      const segments = await transcriptSegments.evaluateAll(extractSegments);
      validateSegments(segments);
      return segments;
    }

    if (!descriptionExpanded) {
      try {
        const expand = tab.playwright.locator(EXPAND_SELECTOR);
        if (await expand.isVisible()) {
          await expand.click();
          descriptionExpanded = true;
        }
      } catch (error) {
        if (!isTransient(error)) throw error;
      }
    }

    if (!transcriptOpened) {
      try {
        const showTranscript = tab.playwright
          .locator(SHOW_TRANSCRIPT_SELECTOR)
          .filter({ visible: true })
          .first();
        if (await showTranscript.isVisible()) {
          await showTranscript.click();
          transcriptOpened = true;
        }
      } catch (error) {
        if (!isTransient(error)) throw error;
      }
    }

    await tab.playwright.waitForTimeout(pollIntervalMs);
  }

  const helperPath = await tab.content.exportYouTubeTranscript();
  return parseHelperExport(await readFile(helperPath, "utf8"));
}
