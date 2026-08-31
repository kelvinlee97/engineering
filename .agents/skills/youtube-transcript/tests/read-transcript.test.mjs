import assert from "node:assert/strict";
import test from "node:test";

import { readYouTubeTranscript } from "../scripts/read-transcript.mjs";

const EXPANDED =
  'ytd-engagement-panel-section-list-renderer[target-id="engagement-panel-searchable-transcript"]' +
  '[visibility="ENGAGEMENT_PANEL_VISIBILITY_EXPANDED"] ytd-transcript-segment-renderer';

function fakeTab({ neverReady = false } = {}) {
  const state = {
    expanded: false,
    hiddenSegments: [{ start_seconds: 0, text: "hidden duplicate" }],
    open: false,
    reads: 0,
    exports: 0,
    tick: 0,
  };
  const visibleSegments = [
    { start_seconds: 3, text: "First" },
    { start_seconds: 8, text: "Second" },
  ];

  const locator = (selector) => {
    const value = {
      filter: () => value,
      first: () => value,
      isVisible: async () => {
        if (selector.includes("#expand")) return !state.expanded;
        if (selector.includes("transcript-section-renderer")) return state.expanded;
        return false;
      },
      click: async () => {
        if (selector.includes("#expand")) {
          if (state.tick === 0) throw new Error("Element is not attached");
          state.expanded = true;
        } else {
          state.open = true;
        }
      },
      count: async () =>
        selector === EXPANDED && state.open && !neverReady && state.tick >= 3
          ? visibleSegments.length
          : 0,
      evaluateAll: async () => {
        state.reads += 1;
        return visibleSegments;
      },
    };
    return value;
  };

  return {
    state,
    tab: {
      content: {
        exportYouTubeTranscript: async () => {
          state.exports += 1;
          return "/tmp/youtube-transcript.txt";
        },
      },
      playwright: {
        locator,
        waitForTimeout: async () => {
          state.tick += 1;
        },
      },
    },
  };
}

test("survives detached controls and reads the expanded transcript once", async () => {
  const { state, tab } = fakeTab();

  const segments = await readYouTubeTranscript(tab, {
    now: () => state.tick * 100,
    pollIntervalMs: 100,
    timeoutMs: 1_000,
  });

  assert.deepEqual(segments, [
    { start_seconds: 3, text: "First" },
    { start_seconds: 8, text: "Second" },
  ]);
  assert.equal(state.reads, 1);
  assert.equal(state.exports, 0);
  assert.equal(segments.includes(state.hiddenSegments[0]), false);
});

test("uses the helper once when transcript segments never mount", async () => {
  const { state, tab } = fakeTab({ neverReady: true });

  const segments = await readYouTubeTranscript(tab, {
    now: () => state.tick * 100,
    pollIntervalMs: 100,
    readFile: async () =>
      "YouTube transcript\nVideo ID: EN7frwQIbKc\nLanguage: en\nCaptions: auto-generated\n\n" +
      "[0:03] First\n[1:02:04] Second",
    timeoutMs: 300,
  });

  assert.deepEqual(segments, [
    { start_seconds: 3, text: "First" },
    { start_seconds: 3724, text: "Second" },
  ]);
  assert.equal(state.reads, 0);
  assert.equal(state.exports, 1);
});

test("default timeout leaves browser execution headroom for the helper", async () => {
  const { state, tab } = fakeTab({ neverReady: true });

  await readYouTubeTranscript(tab, {
    now: () => state.tick * 250,
    readFile: async () => "[0:03] First",
  });

  assert.equal(state.tick, 40);
  assert.equal(state.exports, 1);
});
