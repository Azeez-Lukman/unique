/**
 * Unique Property & Construction Company
 * Vanilla JavaScript UI Interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    // Mobile navigation toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            const isHidden = mobileMenu.classList.contains('hidden');
            if (isHidden) {
                mobileMenu.classList.remove('hidden');
                mobileMenuBtn.setAttribute('aria-expanded', 'true');
            } else {
                mobileMenu.classList.add('hidden');
                mobileMenuBtn.setAttribute('aria-expanded', 'false');
            }
        });
    }

    // Category selector helper for contact links
    const categorySelect = document.querySelector('select[name="category"]');
    const urlParams = new URLSearchParams(window.location.search);
    const categoryParam = urlParams.get('category');
    
    if (categorySelect && categoryParam) {
        for (let option of categorySelect.options) {
            if (option.value === categoryParam) {
                option.selected = true;
                break;
            }
        }
    }

    // Auto-dismiss alert messages after 6 seconds
    const alerts = document.querySelectorAll('.messages-alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 6000);
    });
});
