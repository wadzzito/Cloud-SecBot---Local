const { app, BrowserWindow, Tray, Menu, ipcMain } = require('electron');
const path = require('path');
const axios = require('axios');
const { scheduleEscalation, clearEscalation } = require('./escalation');

const BACKEND_URL = 'http://localhost:8000';
const POLL_INTERVAL_MS = 15000; // cada 15 segundos, ajústalo a tu gusto

let tray = null;
let alertWindow = null;
let dismissedFindings = new Set(); // evita reabrir el mismo hallazgo en el mismo ciclo

app.disableHardwareAcceleration(); // opcional, ayuda en máquinas modestas

function createTray() {
  tray = new Tray(path.join(__dirname, 'assets', 'icon.png'));
  const contextMenu = Menu.buildFromTemplate([
    { label: 'Cloud SecBot activo', enabled: false },
    { type: 'separator' },
    { label: 'Salir', click: () => app.quit() }
  ]);
  tray.setToolTip('Cloud SecBot - Monitoreando');
  tray.setContextMenu(contextMenu);
}

function createAlertWindow(finding) {
  if (alertWindow) return; // ya hay una alerta abierta, no dupliques

  alertWindow = new BrowserWindow({
    fullscreen: true,
    kiosk: true,
    alwaysOnTop: true,
    frame: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true
    }
  });

  alertWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'));

  alertWindow.webContents.once('did-finish-load', () => {
    alertWindow.webContents.send('finding-data', finding);
  });

  alertWindow.on('closed', () => {
    alertWindow = null;
  });
}

async function checkForFindings() {
  try {
    const { data } = await axios.get(`${BACKEND_URL}/findings/pending-alerts/`);
    const urgent = data.filter(f =>
      (f.severity === 'P0' || f.severity === 'P1') &&
      !dismissedFindings.has(f.id)
    );

    if (urgent.length > 0) {
      createAlertWindow(urgent[0]); // muestra uno a la vez
    }
  } catch (err) {
    console.error('No se pudo conectar al backend:', err.message);
  }
}

// --- Comunicación desde la ventana de alerta ---
ipcMain.handle('apply-fix', async (event, findingId) => {
  const { data } = await axios.post(`${BACKEND_URL}/actions/${findingId}/apply-fix`);
  if (alertWindow) alertWindow.close();
  return data;
});

ipcMain.handle('dismiss-finding', async (event, findingId, severity) => {
  await axios.post(`${BACKEND_URL}/actions/${findingId}/dismiss`);
  dismissedFindings.add(findingId);
  if (alertWindow) alertWindow.close();

  scheduleEscalation(severity, () => {
    dismissedFindings.delete(findingId); // vuelve a ser candidato para alerta
  });

  return { ok: true };
});

app.whenReady().then(() => {
  createTray();
  setInterval(checkForFindings, POLL_INTERVAL_MS);
});

app.on('window-all-closed', (e) => {
  e.preventDefault(); // el proceso sigue vivo en el tray, no se cierra la app
});