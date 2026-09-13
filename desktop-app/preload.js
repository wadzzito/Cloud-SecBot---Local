const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('secbot', {
  onFindingData: (callback) => ipcRenderer.on('finding-data', (event, finding) => callback(finding)),
  applyFix: (findingId) => ipcRenderer.invoke('apply-fix', findingId),
  dismissFinding: (findingId, severity) => ipcRenderer.invoke('dismiss-finding', findingId, severity)
});