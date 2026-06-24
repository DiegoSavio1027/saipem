import { toast } from 'vue-sonner';

// Helper: Convert File to Base64
export const fileToBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
};

// Helper: Convert Base64 to Blob
export const base64ToBlob = (base64String, contentType = '') => {
  const parts = base64String.split(';base64,');
  const base64Data = parts[1] || parts[0];
  const byteCharacters = atob(base64Data);
  const byteArrays = [];
  
  for (let offset = 0; offset < byteCharacters.length; offset += 512) {
    const slice = byteCharacters.slice(offset, offset + 512);
    const byteNumbers = new Array(slice.length);
    for (let i = 0; i < slice.length; i++) {
      byteNumbers[i] = slice.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    byteArrays.push(byteArray);
  }
  return new Blob(byteArrays, { type: contentType });
};

// Queue operations
export const getOfflineQueue = () => {
  try {
    const queue = localStorage.getItem('hse_offline_queue');
    return queue ? JSON.parse(queue) : [];
  } catch (e) {
    console.error('Error reading offline queue:', e);
    return [];
  }
};

export const saveOfflineQueue = (queue) => {
  localStorage.setItem('hse_offline_queue', JSON.stringify(queue));
};

export const addToQueue = (type, url, payload, headers = {}) => {
  const queue = getOfflineQueue();
  const newItem = {
    id: 'off-' + Date.now() + '-' + Math.floor(Math.random() * 1000),
    type,
    url,
    payload,
    headers,
    timestamp: new Date().toISOString()
  };
  queue.push(newItem);
  saveOfflineQueue(queue);
  console.log(`[OFFLINE] Item added to queue (${type}):`, newItem.id);
  
  toast.warning("Offline Mode Active", {
    description: "You are offline. Your request has been saved locally and will sync when connection returns."
  });
  return newItem;
};

// Automatic Syncer
let isSyncing = false;

export const syncOfflineQueue = async () => {
  if (isSyncing) return;
  const queue = getOfflineQueue();
  if (queue.length === 0) return;

  isSyncing = true;
  console.log(`[SYNC] Starting offline queue sync: ${queue.length} items...`);
  toast.info("Connection Restored", { description: "Synchronizing offline database requests..." });

  const remainingQueue = [];
  let syncSuccessCount = 0;

  for (const item of queue) {
    try {
      let response;
      
      if (item.type === 'INCIDENT_CREATE') {
        // Rebuild FormData for multipart incident uploads
        const formData = new FormData();
        const { proof_image_base64, proof_image_name, proof_image_type, ...fields } = item.payload;
        
        Object.keys(fields).forEach(key => {
          formData.append(key, fields[key]);
        });
        
        if (proof_image_base64) {
          const blob = base64ToBlob(proof_image_base64, proof_image_type);
          formData.append('proof_image', blob, proof_image_name);
        }

        response = await fetch(item.url, {
          method: 'POST',
          headers: {
            'Authorization': item.headers.Authorization || '',
            'X-CSRFToken': item.headers['X-CSRFToken'] || ''
          },
          body: formData
        });
      } else {
        // Regular JSON post for PTW / START_WORK
        response = await fetch(item.url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': item.headers.Authorization || '',
            'X-CSRFToken': item.headers['X-CSRFToken'] || ''
          },
          body: JSON.stringify(item.payload)
        });
      }

      if (response.ok) {
        syncSuccessCount++;
        console.log(`[SYNC] Successfully synced queue item: ${item.id}`);
      } else {
        const errText = await response.text();
        console.error(`[SYNC] Server rejected item: ${item.id}. Error:`, errText);
        // Keep it in the queue if it's a server failure or retryable issue
        remainingQueue.push(item);
      }
    } catch (error) {
      console.error(`[SYNC] Network error syncing item: ${item.id}`, error);
      remainingQueue.push(item); // Keep to retry later
    }
  }

  saveOfflineQueue(remainingQueue);
  isSyncing = false;

  if (syncSuccessCount > 0) {
    toast.success("Sync Complete", {
      description: `Successfully synchronized ${syncSuccessCount} offline requests to server.`
    });
    // Trigger custom event to notify Vue views to reload
    window.dispatchEvent(new CustomEvent('offline-sync-complete'));
  }
};

// Register online/offline event listeners
if (typeof window !== 'undefined') {
  window.addEventListener('online', () => {
    syncOfflineQueue();
  });
}
