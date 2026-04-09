#!/usr/bin/env node
/**
 * Run a command inside the ODK Docker container with a project directory
 * mounted at /work. Cross-platform (Windows and Mac/Linux).
 *
 * Usage:
 *   node scripts/odk-docker-run.js "<command>"
 *   node scripts/odk-docker-run.js "<project_dir>" "<command>"
 *
 * When project_dir is omitted or empty, uses process.cwd(). When provided
 * (e.g. "projects/pizza" or absolute path), that directory is mounted at /work.
 * Relative project_dir is resolved from the repo root (parent of scripts/).
 *
 * Example (workspace ontology): node scripts/odk-docker-run.js "robot verify --input ontology/edit.owl"
 * Example (clone):             node scripts/odk-docker-run.js "projects/owner-repo" "robot verify --input src/envo/envo-edit.owl"
 */
const path = require('path');
const { spawnSync } = require('child_process');

const argv = process.argv.slice(2);
const repoRoot = path.resolve(__dirname, '..');

function normalizePathForDocker(dirPath) {
  const normalized = path.resolve(dirPath);
  if (process.platform === 'win32') {
    return normalized.replace(/\\/g, '/');
  }
  return normalized;
}

function isBlank(s) {
  if (s == null) return true;
  const t = String(s).trim();
  return t === '' || t === 'undefined';
}

let workDir;
let command;

if (argv.length >= 2 && !isBlank(argv[0])) {
  workDir = path.isAbsolute(argv[0]) ? path.resolve(argv[0]) : path.resolve(repoRoot, argv[0]);
  command = argv[1];
} else if (argv.length === 1) {
  workDir = process.cwd();
  command = argv[0];
} else if (argv.length >= 2 && isBlank(argv[0])) {
  workDir = process.cwd();
  command = argv[1];
} else {
  console.error('Usage: node scripts/odk-docker-run.js "<command>"');
  console.error('   or: node scripts/odk-docker-run.js "<project_dir>" "<command>"');
  process.exit(1);
}

if (!command || (typeof command === 'string' && command.trim() === '')) {
  console.error('Missing command.');
  process.exit(1);
}

const mountSource = normalizePathForDocker(workDir);
const args = [
  'run',
  '-v', `${mountSource}:/work`,
  '-w', '/work',
  '--rm',
  'obolibrary/odkfull',
  'sh', '-c', command
];
const r = spawnSync('docker', args, { stdio: 'inherit', shell: false });
process.exit(r.status !== null ? r.status : 0);
