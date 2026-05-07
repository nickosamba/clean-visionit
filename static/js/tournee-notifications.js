// Notification handler for tournee creation
class TourneeNotification {
    constructor() {
        this.init();
    }

    init() {
        // Request notification permission on initialization
        if ("Notification" in window) {
            Notification.requestPermission().then(permission => {
                if (permission === "granted") {
                    console.log("Notifications autorisées !");
                } else if (permission === "denied") {
                    console.log("Notifications bloquées par l'utilisateur");
                }
            });
        }
    }

    showNotification(title, body, icon = null) {
        if ("Notification" in window && Notification.permission === "granted") {
            const options = {
                body: body,
                icon: icon || "/static/img/logo_clean.png",
                badge: "/static/img/badge.png", // Small badge icon
                tag: "tournee-notification"
            };

            new Notification(title, options);
        } else if ("Notification" in window && Notification.permission !== "denied") {
            // If permission hasn't been granted yet, request it and then show notification
            Notification.requestPermission().then(permission => {
                if (permission === "granted") {
                    const options = {
                        body: body,
                        icon: icon || "/static/img/logo_clean.png",
                        badge: "/static/img/badge.png",
                        tag: "tournee-notification"
                    };
                    
                    new Notification(title, options);
                }
            });
        }
    }

    // Method to trigger notification when a tournee is created
    notifyTourneeCreated(agentName, date, clientId = null) {
        let bodyText = `Agent: ${agentName} - Date: ${date}`;
        if (clientId) {
            bodyText += ` - Client: ${clientId}`;
        }

        this.showNotification(
            "Nouvelle tournée ajoutée 🚀",
            bodyText
        );
    }

    // Method to trigger notification when a tournee client is added
    notifyTourneeClientAdded(clientInfo, date) {
        this.showNotification(
            "Nouveau client ajouté à la tournée 📋",
            `${clientInfo} - Date: ${date}`
        );
    }

    // Method to trigger notification for an agent when a client is assigned to their tournee
    notifyAgentOfNewAssignment(agentName, clientName, tourneeDate) {
        this.showNotification(
            `Nouvelle assignation pour ${agentName} 📋`,
            `Client ${clientName} ajouté à votre tournée du ${tourneeDate}`
        );
    }
}

// Initialize the notification handler
document.addEventListener("DOMContentLoaded", () => {
    window.tourneeNotifier = new TourneeNotification();
});

// Global function to trigger notification from other scripts
function triggerTourneeNotification(agentName, date, clientId = null) {
    if (window.tourneeNotifier) {
        window.tourneeNotifier.notifyTourneeCreated(agentName, date, clientId);
    }
}

// Global function to trigger tournee client notification
function triggerTourneeClientNotification(clientInfo, date) {
    if (window.tourneeNotifier) {
        window.tourneeNotifier.notifyTourneeClientAdded(clientInfo, date);
    }
}

// Global function to trigger agent notification for new assignment
function triggerAgentNotification(agentName, clientName, tourneeDate) {
    if (window.tourneeNotifier) {
        window.tourneeNotifier.notifyAgentOfNewAssignment(agentName, clientName, tourneeDate);
    }
}

// Make TourneeNotification class available globally for agent notifications
window.TourneeNotification = TourneeNotification;