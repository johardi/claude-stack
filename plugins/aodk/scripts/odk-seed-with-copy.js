#!/usr/bin/env node
/**
 * Run ODK seed then copy target/<id>/src into src/.
 * Requires Node 16.7+ (fs.cpSync). Run from project root.
 * Usage: node scripts/odk-seed-with-copy.js <config_path> [extra_seed_args]
 */
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const configPathArg = process.argv[2];
const extra = process.argv.slice(3).join(' ') || '';

if (!configPathArg) {
  console.error('Usage: node scripts/odk-seed-with-copy.js <config_path> [extra_seed_args]');
  process.exit(1);
}

// 1. Run ODK seed in Docker
const seedCmd = `/tools/odk.py seed -c -C ${configPathArg} --gitname "Ontology Builder" --gitemail "builder@local" ${extra}`.trim();
const r = spawnSync('node', [path.join(__dirname, 'odk-docker-run.js'), seedCmd], {
  stdio: 'inherit',
  cwd: process.cwd(),
});
if (r.status !== 0) {
  process.exit(r.status);
}

// 2. Copy target/<id>/src into src/
const projectRoot = process.cwd();
const configPath = configPathArg.startsWith('src/') || configPathArg.startsWith('src\\')
  ? path.join(projectRoot, configPathArg)
  : path.join(projectRoot, 'src', configPathArg);

if (!fs.existsSync(configPath)) {
  console.error('Config file not found:', configPath);
  process.exit(1);
}

const yaml = fs.readFileSync(configPath, 'utf8');
const idMatch = yaml.match(/^id:\s*(\S+)/m);
if (!idMatch) {
  console.error('Could not find "id:" in config:', configPath);
  process.exit(1);
}
const ontologyId = idMatch[1].trim();

const targetSrc = path.join(projectRoot, 'src', 'target', ontologyId, 'src');
if (!fs.existsSync(targetSrc)) {
  console.error('Target src not found after seed:', targetSrc);
  process.exit(1);
}

const copies = [
  { from: 'ontology', to: 'ontology' },
  { from: 'sparql', to: 'sparql' },
  { from: 'metadata', to: 'metadata' },
  { from: 'scripts', to: 'odk-scripts' },
];

for (const { from: dir, to: destDir } of copies) {
  const src = path.join(targetSrc, dir);
  const dest = path.join(projectRoot, 'src', destDir);
  if (!fs.existsSync(src)) continue;
  fs.cpSync(src, dest, { recursive: true, force: true });
  console.log('Copied', dir, '->', 'src/' + destDir);
}

console.log('Done. Ontology', ontologyId, 'is in src/.');
