import { reactive, ref } from 'vue';
import { sendEmergencyAlert, requestNotificationPermission, sendPushNotification } from '@/utils/notifications';
import { toast } from 'vue-sonner';

const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8989';

export const websocketState = reactive({
    isConnected: false,
    liveFeeds: [],
    socket: null
});

export const ptwSocketState = reactive({
    isConnected: false,
    recentPTWs: [],
    socket: null,
    lastUpdate: 0
});

export const incidentsSocketState = reactive({
    isConnected: false,
    recentIncidents: [],
    socket: null,
    lastUpdate: 0
});

export const initializeWebSocket = () => {
    if (websocketState.socket) {
        return;
    }

    requestNotificationPermission();

    websocketState.socket = new WebSocket(`${WS_BASE_URL}/ws/pob_updates/`);

    websocketState.socket.onopen = () => {
        websocketState.isConnected = true;
    };

    websocketState.socket.onmessage = (e) => {
        try {
            const data = JSON.parse(e.data);
            const message = data.message;

            // Check if this is an emergency alert
            if (data.type === 'emergency_alert' && message?.event === 'MUSTER_DRILL_ACTIVATED') {
                // Only trigger notification/sound for employees who are checked in (in active PTWs)
                import('@/store/auth').then(({ authState }) => {
                    const currentUserEmpId = authState.empId;
                    const activePtws = message.active_ptws || [];

                    // Check if current user is in the active PTWs list
                    const isUserCheckedIn = activePtws.some(ptw => ptw.emp_id === currentUserEmpId);

                    if (isUserCheckedIn) {
                        sendEmergencyAlert(
                            message.global_status,
                            message.target_location || 'ALL',
                            message.active_ptws_count || 0
                        );
                    }
                });

                // Add emergency alert to live feeds for everyone
                const emergencyFeed = {
                    action: 'EMERGENCY',
                    employee_name: '🚨 MUSTER DRILL ACTIVATED',
                    location: `${message.global_status} - ${message.target_location || 'ALL LOCATIONS'}`,
                    time: message?.timestamp ? new Date(message.timestamp).toLocaleString() : new Date().toLocaleString(),
                    timestamp: message?.timestamp
                };
                websocketState.liveFeeds.unshift(emergencyFeed);
                return;
            }

            const newFeed = {
                action: message?.action || 'IN',
                employee_name: message?.employee_name || 'Unknown',
                location: message?.location || 'Unknown',
                time: message?.timestamp ? new Date(message.timestamp).toLocaleString() : new Date().toLocaleString(),
                timestamp: message?.timestamp
            };

            // Check for duplicates
            const isDuplicate = websocketState.liveFeeds.some(feed =>
                feed.employee_name === newFeed.employee_name &&
                feed.action === newFeed.action &&
                feed.location === newFeed.location &&
                feed.timestamp === newFeed.timestamp
            );

            if (!isDuplicate) {
                websocketState.liveFeeds.unshift(newFeed);
            }

            if (websocketState.liveFeeds.length > 20) {
                websocketState.liveFeeds.pop();
            }
        } catch (error) {
            console.error('Error parsing WebSocket message:', error);
        }
    };

    websocketState.socket.onclose = () => {
        websocketState.isConnected = false;
        websocketState.socket = null;
        console.log('WebSocket disconnected');
    };

    websocketState.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        websocketState.isConnected = false;
    };
};

export const initializePTWWebSocket = () => {
    if (ptwSocketState.socket) {
        return;
    }

    ptwSocketState.socket = new WebSocket(`${WS_BASE_URL}/ws/ptw_updates/`);

    ptwSocketState.socket.onopen = () => {
        ptwSocketState.isConnected = true;
        ptwSocketState.recentPTWs = [];
    };

    ptwSocketState.socket.onmessage = (e) => {
        try {
            const data = JSON.parse(e.data);
            const message = data.message;

            if (data.type === 'ptw_recent') {
                ptwSocketState.recentPTWs.unshift(message);
                return;
            }

            if (data.type === 'ptw_created') {
                import('@/store/auth').then(({ authState }) => {
                    if (authState.userRole === 'Safety Officer') {
                        sendPushNotification('New PTW Submitted', {
                            body: `${message.employee_name} submitted a new ${message.permit_type} permit`,
                            icon: '/saipem-logo.png',
                            badge: '/saipem-badge.png'
                        });
                        toast.info(`New PTW: ${message.permit_id}`);
                    }
                });
                ptwSocketState.recentPTWs.unshift(message);
                ptwSocketState.lastUpdate = Date.now();
                return;
            }

            if (data.type === 'ptw_status_changed') {
                import('@/store/auth').then(({ authState }) => {
                    const shouldNotify = (message.notify_role === 'Worker' && message.affected_user === authState.empId) ||
                                       (message.notify_role === 'Safety Officer' && authState.userRole === 'Safety Officer');

                    if (shouldNotify) {
                        const statusText = message.event.replace('PTW_', '').replace(/_/g, ' ');
                        sendPushNotification(`PTW ${statusText}`, {
                            body: `Permit ${message.permit_id} has been ${statusText.toLowerCase()}`,
                            icon: '/saipem-logo.png',
                            badge: '/saipem-badge.png'
                        });
                        toast.info(`PTW ${message.permit_id}: ${statusText}`);
                    }
                });
                ptwSocketState.recentPTWs.unshift(message);
                ptwSocketState.lastUpdate = Date.now();
            }
        } catch (error) {
            console.error('Error parsing PTW WebSocket message:', error);
        }
    };

    ptwSocketState.socket.onclose = () => {
        ptwSocketState.isConnected = false;
        ptwSocketState.socket = null;
        console.log('PTW WebSocket disconnected');
    };

    ptwSocketState.socket.onerror = (error) => {
        console.error('PTW WebSocket error:', error);
        ptwSocketState.isConnected = false;
    };
};

export const initializeIncidentsWebSocket = () => {
    if (incidentsSocketState.socket) {
        return;
    }

    incidentsSocketState.socket = new WebSocket(`${WS_BASE_URL}/ws/incidents_updates/`);

    incidentsSocketState.socket.onopen = () => {
        incidentsSocketState.isConnected = true;
        incidentsSocketState.recentIncidents = [];
    };

    incidentsSocketState.socket.onmessage = (e) => {
        try {
            const data = JSON.parse(e.data);
            const message = data.message;

            if (data.type === 'incident_recent') {
                incidentsSocketState.recentIncidents.unshift(message);
                return;
            }

            if (data.type === 'incident_created') {
                import('@/store/auth').then(({ authState }) => {
                    if (authState.userRole === 'Safety Officer') {
                        sendPushNotification('New Incident Report', {
                            body: `${message.employee_name} reported a ${message.severity} incident at ${message.location}`,
                            icon: '/saipem-logo.png',
                            badge: '/saipem-badge.png'
                        });
                        toast.warning(`New Incident: ${message.incident_id}`);
                    }
                });
                incidentsSocketState.recentIncidents.unshift(message);
                incidentsSocketState.lastUpdate = Date.now();
                return;
            }

            if (data.type === 'incident_status_changed') {
                import('@/store/auth').then(({ authState }) => {
                    if (authState.userRole === 'Safety Officer') {
                        const statusText = message.new_status.replace(/_/g, ' ');
                        sendPushNotification('Incident Status Updated', {
                            body: `Incident ${message.incident_id} status changed to ${statusText}`,
                            icon: '/saipem-logo.png',
                            badge: '/saipem-badge.png'
                        });
                        toast.info(`Incident ${message.incident_id}: ${statusText}`);
                    }
                });
                incidentsSocketState.recentIncidents.unshift(message);
                incidentsSocketState.lastUpdate = Date.now();
                return;
            }

            if (data.type === 'system_status_changed') {
                if (message.notify_all) {
                    if (message.global_status === 'RED') {
                        sendEmergencyAlert(
                            message.global_status,
                            'ALL LOCATIONS',
                            0
                        );
                    } else if (message.global_status === 'YELLOW') {
                        sendPushNotification('System Alert', {
                            body: 'System status changed to YELLOW - Extra caution required',
                            icon: '/saipem-logo.png',
                            badge: '/saipem-badge.png'
                        });
                        toast.warning('System status: YELLOW');
                    }
                }
                incidentsSocketState.lastUpdate = Date.now();
            }
        } catch (error) {
            console.error('Error parsing Incidents WebSocket message:', error);
        }
    };

    incidentsSocketState.socket.onclose = () => {
        incidentsSocketState.isConnected = false;
        incidentsSocketState.socket = null;
        console.log('Incidents WebSocket disconnected');
    };

    incidentsSocketState.socket.onerror = (error) => {
        console.error('Incidents WebSocket error:', error);
        incidentsSocketState.isConnected = false;
    };
};

export const closeWebSocket = () => {
    if (websocketState.socket) {
        websocketState.socket.close();
        websocketState.socket = null;
        websocketState.isConnected = false;
    }
};

export const closePTWWebSocket = () => {
    if (ptwSocketState.socket) {
        ptwSocketState.socket.close();
        ptwSocketState.socket = null;
        ptwSocketState.isConnected = false;
    }
};

export const closeIncidentsWebSocket = () => {
    if (incidentsSocketState.socket) {
        incidentsSocketState.socket.close();
        incidentsSocketState.socket = null;
        incidentsSocketState.isConnected = false;
    }
};

export const clearLiveFeeds = () => {
    websocketState.liveFeeds = [];
};
