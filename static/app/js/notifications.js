/**
 * Gestão de Notificações Web Push para CRM Intalog
 */

const WebPushManager = {
    swRegistration: null,
    isSubscribed: false,
    
    // Configurações passadas pelo Django (serão injetadas no HTML)
    vapidPublicKey: window.WEBPUSH_PUBLIC_KEY,

    async init() {
        if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
            console.warn('Push messaging is not supported');
            return;
        }

        try {
            this.swRegistration = await navigator.serviceWorker.ready;
            const subscription = await this.swRegistration.pushManager.getSubscription();
            this.isSubscribed = !(subscription === null);
            
            this.updateUI();
            this.checkFirstVisit();
        } catch (error) {
            console.error('Error during notification init:', error);
        }
    },

    updateUI() {
        const switchInput = document.getElementById('notificationSwitch');
        if (switchInput) {
            switchInput.checked = this.isSubscribed;
            switchInput.onchange = () => this.toggleSubscription();
        }
    },

    checkFirstVisit() {
        const hasDecided = localStorage.getItem('notificationDecided');
        if (!hasDecided && !this.isSubscribed) {
            this.showBanner();
        }
    },

    showBanner() {
        if (document.getElementById('notificationBanner')) return;

        const banner = document.createElement('div');
        banner.id = 'notificationBanner';
        banner.className = 'alert alert-dark position-fixed bottom-0 start-50 translate-middle-x mb-3 shadow-lg d-flex align-items-center justify-content-between p-3';
        banner.style.zIndex = '9999';
        banner.style.minWidth = '320px';
        banner.style.borderRadius = '12px';
        banner.style.border = '1px solid #444';
        
        banner.innerHTML = `
            <div class="me-3">
                <i class="bi bi-bell-fill text-warning me-2"></i>
                <span>Receber avisos de metas?</span>
            </div>
            <div class="d-flex gap-2">
                <button class="btn btn-sm btn-outline-light" id="btnNotifNo">Não</button>
                <button class="btn btn-sm btn-primary" id="btnNotifYes">Sim</button>
            </div>
        `;
        
        document.body.appendChild(banner);

        document.getElementById('btnNotifNo').onclick = () => {
            localStorage.setItem('notificationDecided', 'true');
            banner.remove();
        };

        document.getElementById('btnNotifYes').onclick = async () => {
            banner.remove();
            await this.subscribeUser();
        };
    },

    async toggleSubscription() {
        const switchInput = document.getElementById('notificationSwitch');
        if (switchInput.checked) {
            await this.subscribeUser();
        } else {
            await this.unsubscribeUser();
        }
    },

    async subscribeUser() {
        console.log("Iniciando processo de inscrição...");
        try {
            const permission = await Notification.requestPermission();
            if (permission !== 'granted') {
                alert('Permissão de notificação negada pelo navegador.');
                this.updateUI();
                return;
            }

            if (!this.vapidPublicKey) {
                console.error("ERRO: VAPID_PUBLIC_KEY não definida.");
                return;
            }

            const subscription = await this.swRegistration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: this.urlB64ToUint8Array(this.vapidPublicKey)
            });

            console.log("Inscrição obtida do navegador:", subscription);
            await this.saveSubscription(subscription);
            
            this.isSubscribed = true;
            localStorage.setItem('notificationDecided', 'true');
            this.updateUI();
        } catch (error) {
            console.error('Falha ao inscrever usuário:', error);
            this.updateUI();
        }
    },

    async unsubscribeUser() {
        try {
            const subscription = await this.swRegistration.pushManager.getSubscription();
            if (subscription) {
                await subscription.unsubscribe();
                await this.saveSubscription(subscription, 'unsubscribe');
            }
            this.isSubscribed = false;
            this.updateUI();
        } catch (error) {
            console.error('Erro ao cancelar inscrição:', error);
        }
    },

    async saveSubscription(subscription, action = 'subscribe') {
        console.log(`Enviando ${action} para o servidor...`);
        
        const subData = subscription.toJSON ? subscription.toJSON() : subscription;
        
        const payload = {
            status_type: action,
            subscription: subData, // Volta a ser objeto
            group: 'metas',
            browser: navigator.userAgent.includes('Chrome') ? 'chrome' : 'firefox',
            user_agent: navigator.userAgent
        };

        try {
            const response = await fetch('/webpush/save_information', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken'),
                },
                body: JSON.stringify(payload)
            });
            
            if (response.ok) {
                console.log(`Sucesso: ${action} salva no servidor!`);
            } else {
                const errText = await response.text();
                console.error("Erro no servidor:", response.status, errText);
            }
        } catch (error) {
            console.error("Erro na requisição:", error);
        }
    },

    urlB64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding)
            .replace(/\-/g, '+')
            .replace(/_/g, '/');

        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);

        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    },

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
};

// Inicializa quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => WebPushManager.init());
