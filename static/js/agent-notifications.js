// Agent notification system for checking new assignments
class AgentNotificationSystem {
    constructor() {
        this.lastChecked = new Date();
        this.pollingInterval = 30000; // Check every 30 seconds
        this.isActive = false;
        this.init();
    }

    init() {
        // Request notification permission
        if ("Notification" in window) {
            Notification.requestPermission().then(permission => {
                if (permission === "granted") {
                    console.log("Agent notifications autorisées !");
                    this.startPolling();
                }
            });
        }
    }

    startPolling() {
        if (this.isActive) return;
        
        this.isActive = true;
        this.pollForAssignments();
    }

    pollForAssignments() {
        if (!this.isActive) return;

        fetch('/tournees/api/check_assignments/')
            .then(response => response.json())
            .then(data => {
                if (data.assignments && data.assignments.length > 0) {
                    // Show notification for each new assignment
                    data.assignments.forEach(assignment => {
                        this.showAssignmentNotification(
                            assignment.client_name,
                            assignment.tournee_date
                        );
                    });
                }
            })
            .catch(error => {
                console.error('Error checking assignments:', error);
            })
            .finally(() => {
                // Schedule next check
                setTimeout(() => this.pollForAssignments(), this.pollingInterval);
            });
    }

    showAssignmentNotification(clientName, tourneeDate) {
        if ("Notification" in window && Notification.permission === "granted") {
            new Notification(`Nouvelle assignation 📋`, {
                body: `Client ${clientName} ajouté à votre tournée du ${tourneeDate}`,
                icon: "/static/img/logo_clean.png",
                tag: `assignment-${Date.now()}`
            });
        }
    }

    stopPolling() {
        this.isActive = false;
    }
}

// Initialize agent notification system if user is an agent
document.addEventListener("DOMContentLoaded", () => {
    // Check if the current user is an agent by looking for agent-specific elements or roles
    // Since we're on the base_agent.html template, we know this is an agent page
    if (document.querySelector('nav [href*="agent"]')) {  // Check if agent-specific navigation exists
        window.agentNotificationSystem = new AgentNotificationSystem();
    }
});