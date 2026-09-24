const test = require('node:test');
const assert = require('node:assert/strict');
const { issueLabels, sizeLabel, staleSizeLabels, AREA_RULES, TYPE_RULES } = require('./triage.js');

test('area rules match their own topic', () => {
  const cases = {
    'area: aws': 'EKS node cannot attach an ENI',
    'area: kubernetes': 'kubectl shows the pod stuck in ContainerCreating',
    'area: linux': 'nginx fails to start under systemd',
    'area: dev-tools': 'Ghostty theme looks wrong on macOS',
    'area: languages': 'ZooKeeper client for Node.js',
    'area: youtube': 'transcript capture drops the last subtitle',
    'area: site': 'quartz build fails on the CSS',
    'area: tooling': 'the validate script rejects a valid page',
  };
  for (const [label, title] of Object.entries(cases)) {
    assert.ok(issueLabels({ title }).includes(label), `${title} -> ${label}`);
  }
});

test('an issue with no area match gets needs-triage', () => {
  assert.deepEqual(issueLabels({ title: 'Hello there', body: '' }), ['needs-triage']);
});

test('needs-triage is not added when an area matched', () => {
  const labels = issueLabels({ title: 'Kubernetes pod crash' });
  assert.ok(labels.includes('area: kubernetes'));
  assert.ok(!labels.includes('needs-triage'));
});

test('type labels are kept even without an area match', () => {
  const labels = issueLabels({ title: 'This is broken', body: '' });
  assert.deepEqual(labels, ['needs-triage', 'bug']);
});

test('an issue can carry several area labels', () => {
  const labels = issueLabels({ title: 'EKS', body: 'kubectl output' });
  assert.deepEqual(labels, ['area: aws', 'area: kubernetes']);
});

test('the body is searched as well as the title', () => {
  assert.ok(issueLabels({ title: 'Question', body: 'this is broken' }).includes('bug'));
});

test('matching is case insensitive', () => {
  assert.ok(issueLabels({ title: 'NGINX + Ubuntu' }).includes('area: linux'));
});

test('a missing body does not throw', () => {
  assert.doesNotThrow(() => issueLabels({ title: 'no body' }));
  assert.doesNotThrow(() => issueLabels({}));
});

test('word-boundary rules do not fire on substrings', () => {
  // "cipher" contains "ci", "deposit" contains "s3"? no - guard the real ones.
  const labels = issueLabels({ title: 'decide on precision', body: 'no topic here' });
  assert.deepEqual(labels, ['needs-triage']);
});

test('label names in the rule tables are unique', () => {
  const names = [...AREA_RULES, ...TYPE_RULES].map(([name]) => name);
  assert.equal(new Set(names).size, names.length);
});

test('size buckets cover their boundaries', () => {
  assert.equal(sizeLabel(0, 0), 'size/XS');
  assert.equal(sizeLabel(19, 0), 'size/XS');
  assert.equal(sizeLabel(20, 0), 'size/S');
  assert.equal(sizeLabel(99, 0), 'size/S');
  assert.equal(sizeLabel(50, 50), 'size/M');
  assert.equal(sizeLabel(399, 0), 'size/M');
  assert.equal(sizeLabel(400, 0), 'size/L');
  assert.equal(sizeLabel(999, 0), 'size/L');
  assert.equal(sizeLabel(1000, 0), 'size/XL');
  assert.equal(sizeLabel(5000, 5000), 'size/XL');
});

test('stale size labels are exactly the other size labels', () => {
  assert.deepEqual(staleSizeLabels(['size/L', 'bug', 'area: site'], 'size/XS'), ['size/L']);
  assert.deepEqual(staleSizeLabels(['size/XS', 'bug'], 'size/XS'), []);
  assert.deepEqual(staleSizeLabels([], 'size/M'), []);
  assert.deepEqual(staleSizeLabels(['size/S', 'size/M'], 'size/L'), ['size/S', 'size/M']);
});
