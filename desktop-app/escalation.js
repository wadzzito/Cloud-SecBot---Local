const ESCALATION_DELAYS_MS = {
  P0: 10 * 60 * 1000,   // 10 minutos
  P1: 60 * 60 * 1000,   // 1 hora
  P2: null,             // no reaparece fullscreen
  P3: null
};

let activeTimers = {};

function scheduleEscalation(severity, onEscalate) {
  const delay = ESCALATION_DELAYS_MS[severity];
  if (!delay) return; // P2/P3 no escalan a pantalla completa

  const timer = setTimeout(() => {
    onEscalate();
  }, delay);

  activeTimers[severity] = timer;
}

function clearEscalation(severity) {
  if (activeTimers[severity]) {
    clearTimeout(activeTimers[severity]);
    delete activeTimers[severity];
  }
}

module.exports = { scheduleEscalation, clearEscalation };