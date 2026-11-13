/**
 * Unique Property & Construction Company
 * Vanilla JavaScript UI Interactions & Brand Select Component
 */

document.addEventListener('DOMContentLoaded', () => {
    // ----------------------------------------------------
    // 1. Mobile Navigation Toggle
    // ----------------------------------------------------
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

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

    // ----------------------------------------------------
    // 2. Custom Brand-Styled Select Dropdowns
    // Replaces default OS blue with official Deep Forest Green & Gold palette
    // ----------------------------------------------------
    const selectElements = document.querySelectorAll('select[name="category"], select.brand-select');

    // Check for category in URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const categoryParam = urlParams.get('category');

    selectElements.forEach(select => {
        // If pre-selected from URL, update native select first
        if (categoryParam) {
            for (let option of select.options) {
                if (option.value === categoryParam) {
                    option.selected = true;
                    break;
                }
            }
        }

        // Hide native select visually but keep it functional for form submission
        select.classList.add('hidden');

        // Create custom dropdown wrapper
        const wrapper = document.createElement('div');
        wrapper.className = 'relative w-full custom-brand-select-wrapper text-left block';
        wrapper.style.width = '100%';

        // Trigger Button
        const trigger = document.createElement('button');
        trigger.type = 'button';
        trigger.className = 'w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-brand-charcoal text-sm flex items-center justify-between cursor-pointer focus:outline-none focus:border-brand-green focus:ring-1 focus:ring-brand-green transition shadow-sm text-left';
        trigger.style.width = '100%';
        trigger.style.boxSizing = 'border-box';
        
        const currentSelectedOption = select.options[select.selectedIndex] || select.options[0];
        
        const labelSpan = document.createElement('span');
        labelSpan.className = 'selected-label font-medium text-brand-charcoal truncate';
        labelSpan.textContent = currentSelectedOption ? currentSelectedOption.text : 'Select an option';

        const chevron = document.createElement('span');
        chevron.className = 'chevron-icon transition-transform duration-200 ml-2 text-brand-green flex-shrink-0';
        chevron.innerHTML = `
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
        `;

        trigger.appendChild(labelSpan);
        trigger.appendChild(chevron);

        // Options List Container - Guaranteed Full-Width of the Input
        const menu = document.createElement('div');
        menu.className = 'custom-options-menu absolute left-0 right-0 w-full min-w-full mt-1.5 bg-white border border-brand-border rounded-xl shadow-2xl z-50 overflow-hidden py-1 max-h-64 overflow-y-auto hidden';
        menu.style.width = '100%';
        menu.style.minWidth = '100%';
        menu.style.left = '0';
        menu.style.right = '0';
        menu.style.boxSizing = 'border-box';

        // Populate options matching brand palette
        Array.from(select.options).forEach(option => {
            const item = document.createElement('div');
            item.dataset.value = option.value;
            item.className = 'option-item w-full px-4 py-3 text-sm cursor-pointer flex items-center justify-between transition';
            item.style.width = '100%';
            item.style.boxSizing = 'border-box';
            
            const itemText = document.createElement('span');
            itemText.textContent = option.text;
            item.appendChild(itemText);

            const isSelected = option.selected;
            if (isSelected) {
                item.classList.add('bg-brand-green', 'text-white', 'font-semibold', 'is-selected');
                const checkIcon = document.createElement('span');
                checkIcon.className = 'check-indicator text-brand-gold flex-shrink-0 ml-2';
                checkIcon.innerHTML = `
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
                    </svg>
                `;
                item.appendChild(checkIcon);
            } else {
                item.classList.add('text-brand-charcoal', 'hover:bg-brand-green-subtle', 'hover:text-brand-green');
            }

            // Option Click Handler
            item.addEventListener('click', (e) => {
                e.stopPropagation();
                select.value = option.value;
                select.dispatchEvent(new Event('change', { bubbles: true }));

                labelSpan.textContent = option.text;

                // Update styling of all items
                menu.querySelectorAll('.option-item').forEach(el => {
                    el.classList.remove('bg-brand-green', 'text-white', 'font-semibold', 'is-selected');
                    el.classList.add('text-brand-charcoal', 'hover:bg-brand-green-subtle', 'hover:text-brand-green');
                    const existingCheck = el.querySelector('.check-indicator');
                    if (existingCheck) existingCheck.remove();
                });

                item.classList.remove('text-brand-charcoal', 'hover:bg-brand-green-subtle', 'hover:text-brand-green');
                item.classList.add('bg-brand-green', 'text-white', 'font-semibold', 'is-selected');
                const checkIcon = document.createElement('span');
                checkIcon.className = 'check-indicator text-brand-gold flex-shrink-0 ml-2';
                checkIcon.innerHTML = `
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
                    </svg>
                `;
                item.appendChild(checkIcon);

                closeMenu();
            });

            menu.appendChild(item);
        });

        function openMenu() {
            // Close any other open menus
            document.querySelectorAll('.custom-options-menu').forEach(m => m.classList.add('hidden'));
            document.querySelectorAll('.chevron-icon').forEach(c => c.classList.remove('rotate-180'));
            
            menu.classList.remove('hidden');
            chevron.classList.add('rotate-180');
            trigger.classList.add('border-brand-green', 'ring-1', 'ring-brand-green');
        }

        function closeMenu() {
            menu.classList.add('hidden');
            chevron.classList.remove('rotate-180');
            trigger.classList.remove('border-brand-green', 'ring-1', 'ring-brand-green');
        }

        trigger.addEventListener('click', (e) => {
            e.stopPropagation();
            if (menu.classList.contains('hidden')) {
                openMenu();
            } else {
                closeMenu();
            }
        });

        // Assemble custom select
        wrapper.appendChild(trigger);
        wrapper.appendChild(menu);
        select.parentNode.insertBefore(wrapper, select);
        wrapper.appendChild(select); // keep in wrapper for neat layout
    });

    // Close custom dropdowns on click outside or Escape
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.custom-brand-select-wrapper')) {
            document.querySelectorAll('.custom-options-menu').forEach(m => m.classList.add('hidden'));
            document.querySelectorAll('.chevron-icon').forEach(c => c.classList.remove('rotate-180'));
            document.querySelectorAll('.custom-brand-select-wrapper button').forEach(b => {
                b.classList.remove('border-brand-green', 'ring-1', 'ring-brand-green');
            });
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.custom-options-menu').forEach(m => m.classList.add('hidden'));
            document.querySelectorAll('.chevron-icon').forEach(c => c.classList.remove('rotate-180'));
        }
    });

    // ----------------------------------------------------
    // 3. Auto-Dismiss Alert Messages
    // ----------------------------------------------------
    const alerts = document.querySelectorAll('.messages-alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 6000);
    });

    // ----------------------------------------------------
    // 4. Reliable Email Link Click & Copy-to-Clipboard Handler
    // Ensures clicking always succeeds even if OS has no default desktop mail client
    // ----------------------------------------------------
    const emailLinks = document.querySelectorAll('a[href^="mailto:"]');
    emailLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const email = link.getAttribute('href').replace('mailto:', '').split('?')[0];
            
            // Copy to clipboard as guaranteed fallback/convenience
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(email).then(() => {
                    showToast(`Copied to clipboard: ${email}`);
                }).catch(() => {});
            }
        });
    });

    function showToast(message) {
        let toast = document.getElementById('global-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'global-toast';
            toast.className = 'fixed bottom-6 right-6 z-50 bg-brand-green-dark text-white px-5 py-3 rounded-xl shadow-2xl border border-brand-gold/40 text-xs sm:text-sm font-medium flex items-center gap-3 transition-all transform duration-300 translate-y-10 opacity-0 pointer-events-none';
            document.body.appendChild(toast);
        }

        toast.innerHTML = `
            <svg class="w-4 h-4 text-brand-gold flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
            </svg>
            <span>${message}</span>
        `;
        toast.classList.remove('translate-y-10', 'opacity-0');
        toast.classList.add('translate-y-0', 'opacity-100');

        setTimeout(() => {
            toast.classList.remove('translate-y-0', 'opacity-100');
            toast.classList.add('translate-y-10', 'opacity-0');
        }, 3500);
    }
});
