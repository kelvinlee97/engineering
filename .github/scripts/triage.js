// Pure labelling logic for .github/workflows/triage.yml.
//
// Kept free of Octokit and the Actions runtime so it can be unit tested with
// `node --test .github/scripts/triage.test.js`. The workflow requires this
// file and only performs the API calls.

const AREA_RULES = [
  ['area: aws', /\baws\b|ec2|eks|\bvpc\b|\beni\b|\bs3\b|cloudformation/],
  ['area: kubernetes', /kubernetes|k8s|kubectl|kubelet|\bpod\b|helm/],
  ['area: linux', /\bbash\b|shell|ubuntu|nginx|systemd|\bapt\b/],
  ['area: dev-tools', /\bgit\b|ghostty|claude|macos|\bterminal\b/],
  ['area: languages', /python|node\.?js|npm|zookeeper|\buv\b/],
  ['area: youtube', /youtube|transcript|subtitle/],
  ['area: site', /mkdocs|\bsite\b|\bcss\b|\bpages\b|\btheme\b/],
  ['area: tooling', /\bci\b|workflow|github action|\bscript\b|validate/],
];

const TYPE_RULES = [
  ['translation', /translat|chinese|中文|readme_zh|bilingual/],
  ['bug', /\bbug\b|broken|\berror\b|\bfails?\b|typo|incorrect|404/],
  ['enhancement', /feature request|\bproposal\b|would be nice|please add|new article/],
  ['question', /^how |\bhow do i\b|\bquestion\b|\?\s*$/m],
];

const SIZE_THRESHOLDS = [
  [20, 'size/XS'],
  [100, 'size/S'],
  [400, 'size/M'],
  [1000, 'size/L'],
];

/**
 * Labels for a newly opened issue.
 * @param {{title?: string, body?: string}} issue
 * @returns {string[]} labels, always including an area label or `needs-triage`
 */
function issueLabels(issue) {
  const text = `${issue.title || ''}\n${issue.body || ''}`.toLowerCase();
  const match = (rules) => rules.filter(([, re]) => re.test(text)).map(([name]) => name);
  const areas = match(AREA_RULES);
  const types = match(TYPE_RULES);
  return areas.length > 0 ? [...areas, ...types] : ['needs-triage', ...types];
}

/**
 * Size bucket for a pull request.
 * @param {number} additions
 * @param {number} deletions
 * @returns {string} one of size/XS, size/S, size/M, size/L, size/XL
 */
function sizeLabel(additions, deletions) {
  const changed = additions + deletions;
  for (const [limit, label] of SIZE_THRESHOLDS) {
    if (changed < limit) return label;
  }
  return 'size/XL';
}

/**
 * Size labels currently on a PR that should be removed.
 * @param {string[]} current every label name on the PR
 * @param {string} wanted the size label the PR should carry
 * @returns {string[]} stale size labels
 */
function staleSizeLabels(current, wanted) {
  return current.filter((name) => name.startsWith('size/') && name !== wanted);
}

module.exports = { issueLabels, sizeLabel, staleSizeLabels, AREA_RULES, TYPE_RULES };
