let currentFinding = null;

window.secbot.onFindingData((finding) => {
  currentFinding = finding;

  document.getElementById('severityBadge').textContent = finding.severity;
  document.getElementById('severityBadge').classList.add(`severity-${finding.severity}`);
  document.getElementById('title').textContent = finding.rule_description || 'Vulnerabilidad detectada';
  document.getElementById('fileInfo').textContent = `${finding.file_path} — línea ${finding.line_number ?? '?'}`;
  document.getElementById('riskText').textContent = finding.riesgo_si_no_se_corrige || 'Revisa este hallazgo antes de continuar.';
});

document.getElementById('applyBtn').addEventListener('click', async () => {
  if (!currentFinding) return;
  await window.secbot.applyFix(currentFinding.id);
});

document.getElementById('dismissBtn').addEventListener('click', async () => {
  if (!currentFinding) return;
  await window.secbot.dismissFinding(currentFinding.id, currentFinding.severity);
});