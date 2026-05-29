// Trigger device vibration
export const triggerVibration = () => {
  if (!('vibrate' in navigator)) {
    return;
  }

  try {
    const pattern = [200, 100, 200, 100, 200];
    navigator.vibrate(pattern);
  } catch (error) {
    console.error('Error triggering vibration:', error);
  }
};

export const requestNotificationPermission = async () => {
  if (!('Notification' in window)) {
    return false;
  }

  if (Notification.permission === 'granted') {
    return true;
  }

  if (Notification.permission !== 'denied') {
    const permission = await Notification.requestPermission();
    return permission === 'granted';
  }

  return false;
};

// Send push notification
export const sendPushNotification = (title, options = {}) => {
  if (Notification.permission === 'granted') {
    const notification = new Notification(title, {
      icon: '/saipem-logo.png',
      badge: '/saipem-badge.png',
      ...options
    });

    setTimeout(() => notification.close(), 10000);
    return notification;
  }
};

// Audio context and alarm audio instance
let audioContext = null;
let alarmAudio = null;
let audioUnlocked = false;

// Initialize audio on first user interaction
export const initializeAudio = async () => {
  if (audioUnlocked) return;

  try {
    // Create and unlock AudioContext
    if (!audioContext) {
      audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }

    if (audioContext.state === 'suspended') {
      await audioContext.resume();
    }

    // Pre-load alarm audio
    if (!alarmAudio) {
      alarmAudio = new Audio(new URL('@/assets/alarm.mp3', import.meta.url).href);
      alarmAudio.volume = 0.8;
      alarmAudio.load();
    }

    audioUnlocked = true;
    console.log('Audio initialized and unlocked');
  } catch (error) {
    console.error('Error initializing audio:', error);
  }
};

// Play emergency sound warning
export const playEmergencySound = async () => {
  // Try to initialize audio if not already done
  if (!audioUnlocked) {
    await initializeAudio();
  }

  try {
    if (alarmAudio) {
      alarmAudio.currentTime = 0;
      alarmAudio.loop = true;
      await alarmAudio.play();

      // Stop after 60 seconds
      setTimeout(() => {
        alarmAudio.pause();
        alarmAudio.currentTime = 0;
      }, 60000);
    }
  } catch (error) {
    console.error('Error playing alarm audio:', error);
    // Fallback to generated tone if audio file fails
    try {
      if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
      }

      if (audioContext.state === 'suspended') {
        await audioContext.resume();
      }

      const now = audioContext.currentTime;

      // Create repeating alarm pattern (10 repeats for ~6 seconds)
      for (let repeat = 0; repeat < 10; repeat++) {
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        oscillator.frequency.value = 1000;
        oscillator.type = 'sine';

        const startTime = now + (repeat * 0.6);
        gainNode.gain.setValueAtTime(0.3, startTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + 0.1);
        gainNode.gain.setValueAtTime(0.3, startTime + 0.15);
        gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + 0.25);
        gainNode.gain.setValueAtTime(0.3, startTime + 0.3);
        gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + 0.4);

        oscillator.start(startTime);
        oscillator.stop(startTime + 0.4);
      }
    } catch (fallbackError) {
      console.error('Error playing fallback sound:', fallbackError);
    }
  }
};

// Send emergency alert notification
export const sendEmergencyAlert = (status, location, activeWorkers) => {
  const title = `🚨 MUSTER DRILL ACTIVATED`;
  const body = `${status === 'RED' ? 'CONDITION RED - EMERGENCY' : 'CONDITION YELLOW - WARNING'}\nLocation: ${location}\nActive Workers: ${activeWorkers}`;

  sendPushNotification(title, {
    body: body,
    tag: 'emergency-alert',
    requireInteraction: true
  });

  // Show visual alert as fallback
  showEmergencyAlert(title, body);

  // Play alarm sound
  playEmergencySound();

  // Trigger device vibration
  triggerVibration();
};

// Show visual emergency alert (fallback if notification doesn't show)
export const showEmergencyAlert = (title, body) => {
  console.log('📍 Showing visual emergency alert');

  // Create alert element
  const alertDiv = document.createElement('div');
  alertDiv.id = 'emergency-alert-visual';
  alertDiv.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
    color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 10px 40px rgba(220, 38, 38, 0.5);
    z-index: 9999;
    max-width: 400px;
    font-family: system-ui, -apple-system, sans-serif;
    animation: slideIn 0.3s ease-out;
  `;

  alertDiv.innerHTML = `
    <div style="font-weight: bold; font-size: 18px; margin-bottom: 8px;">${title}</div>
    <div style="font-size: 14px; white-space: pre-wrap;">${body}</div>
    <button onclick="this.parentElement.remove()" style="
      margin-top: 12px;
      background: rgba(255,255,255,0.2);
      border: 1px solid rgba(255,255,255,0.3);
      color: white;
      padding: 8px 16px;
      border-radius: 4px;
      cursor: pointer;
      font-weight: 500;
    ">Dismiss</button>
  `;

  document.body.appendChild(alertDiv);

  // Auto remove after 15 seconds
  setTimeout(() => {
    if (alertDiv.parentElement) {
      alertDiv.remove();
    }
  }, 15000);
};

// Add animation
if (!document.querySelector('style[data-emergency-alert]')) {
  const style = document.createElement('style');
  style.setAttribute('data-emergency-alert', 'true');
  style.textContent = `
    @keyframes slideIn {
      from {
        transform: translateX(400px);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
  `;
  document.head.appendChild(style);
}
