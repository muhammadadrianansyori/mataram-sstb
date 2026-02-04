/**
 * Main Application Script
 */

document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

function initApp() {
    // 1. Populate Metadata
    const metadata = window.Logic.generateMockMetadata();
    document.getElementById('satRefId').value = metadata.referenceId;
    document.getElementById('detectTime').value = metadata.timestamp;

    // 2. Bind Events
    bindStructureTypeParams();
    bindCamera();
    bindGPS();
    bindFormSubmit();
}

function bindStructureTypeParams() {
    const radioInputs = document.querySelectorAll('input[name="structureType"]');
    const dimensionalSection = document.getElementById('dimensionalSection');

    radioInputs.forEach(radio => {
        radio.addEventListener('change', (e) => {
            const selectedValue = e.target.value;
            const visibility = window.Logic.getSectionVisibility(selectedValue);

            if (visibility.dimensionalAnalysis) {
                dimensionalSection.classList.remove('hidden');
                // Optional: animation slide down logic could go here
                dimensionalSection.style.display = 'block';
                setTimeout(() => dimensionalSection.style.opacity = '1', 10);
            } else {
                dimensionalSection.style.opacity = '0';
                setTimeout(() => {
                    dimensionalSection.classList.add('hidden');
                    dimensionalSection.style.display = 'none';
                }, 300); // Wait for transition
            }
        });
    });
}

function bindCamera() {
    const btn = document.getElementById('cameraBtn');
    const input = document.getElementById('roofPhoto');
    const label = document.getElementById('fileName');

    btn.addEventListener('click', () => {
        input.click();
    });

    input.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
            label.textContent = e.target.files[0].name;
            label.style.color = 'var(--text-main)';
        }
    });
}

function bindGPS() {
    const btn = document.getElementById('gpsBtn');
    const input = document.getElementById('gpsLocation');

    btn.addEventListener('click', () => {
        btn.innerHTML = 'Locking...';

        // Browser Geolocation API
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const { latitude, longitude, accuracy } = position.coords;
                    input.value = `${latitude.toFixed(6)}, ${longitude.toFixed(6)} (±${Math.round(accuracy)}m)`;
                    btn.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
                        Locked
                    `;
                    btn.classList.add('btn-success');
                    // Reset styling if needed
                    btn.style.borderColor = 'var(--success-color)';
                    btn.style.color = 'var(--success-color)';
                },
                (error) => {
                    console.error("GPS Error: ", error);
                    // Fallback for simulation if permission denied or error
                    simulateGPS(input, btn);
                },
                { enableHighAccuracy: true, timeout: 5000 }
            );
        } else {
            simulateGPS(input, btn);
        }
    });
}

function simulateGPS(input, btn) {
    // Fallback simulation for dev environment without GPS
    setTimeout(() => {
        const lat = -8.583069 + (Math.random() * 0.01);
        const lng = 116.116508 + (Math.random() * 0.01);
        input.value = `${lat.toFixed(6)}, ${lng.toFixed(6)} (Simulated)`;
        btn.innerHTML = 'Locked (Sim)';
        btn.style.color = 'var(--accent-color)';
        btn.style.borderColor = 'var(--accent-color)';
    }, 1000);
}

function bindFormSubmit() {
    const form = document.getElementById('verificationForm');

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const errors = window.Logic.validate(formData);

        if (errors.length > 0) {
            alert(errors.join('\n'));
            return;
        }

        // Success Feedback
        const btn = form.querySelector('button[type="submit"]');
        const originalText = btn.innerText;

        btn.innerText = 'Submitting...';
        btn.disabled = true;

        setTimeout(() => {
            alert('Verification Data Saved Successfully!');
            btn.innerText = originalText;
            btn.disabled = false;
            // form.reset(); // Optional: reset form
        }, 1500);
    });
}
