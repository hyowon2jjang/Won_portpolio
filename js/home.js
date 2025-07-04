document.addEventListener('DOMContentLoaded', () => {
    // Get the parent container
    const experienceContainer = document.querySelector('.world-experience-container');
    const worldMap = document.getElementById('worldMap');
    const experienceCards = document.querySelectorAll('.experience-card');
    const mapPoints = document.querySelectorAll('.map-point');

    const locations = {
        'seoul': { x: 82.5, y: 40, zoom: 5 },
        'warsaw': { x: 52, y: 40, zoom: 4 },
        'waterloo': { x: 26, y: 35, zoom: 4 }
    };

    function updateMap(locationId) {
        const location = locations[locationId];

        if (location) {
            // Add 'is-active' class to the container when a location is selected
            experienceContainer.classList.add('location-active');

            worldMap.style.setProperty('--map-origin-x', `${location.x}%`);
            worldMap.style.setProperty('--map-origin-y', `${location.y}%`);
            worldMap.style.setProperty('--map-zoom', location.zoom);

            const panX = (50 - location.x) * (location.zoom * 0.1);
            const panY = (50 - location.y) * (location.zoom * 0.1);
            worldMap.style.setProperty('--map-pan-x', `${panX}%`);
            worldMap.style.setProperty('--map-pan-y', `${panY}%`);

        } else {
            // Remove 'is-active' class when no location is selected
            experienceContainer.classList.remove('location-active');

            worldMap.style.setProperty('--map-zoom', 1);
            worldMap.style.setProperty('--map-pan-x', '0%');
            worldMap.style.setProperty('--map-pan-y', '0%');
        }

        mapPoints.forEach(point => {
            point.classList.toggle('active', point.dataset.locationId === locationId);
        });

        experienceCards.forEach(card => {
            card.classList.toggle('active', card.dataset.location === locationId);
        });
    }

    // ... The rest of your JS file (observer, event listeners) remains the same ...

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                updateMap(entry.target.dataset.location);
            }
        });
    }, {
        rootMargin: '-50% 0px -50% 0px',
        threshold: 0
    });

    experienceCards.forEach(card => observer.observe(card));

    mapPoints.forEach(point => {
        point.addEventListener('click', () => {
            const locationId = point.dataset.locationId;
            const targetCard = document.querySelector(`.experience-card[data-location="${locationId}"]`);
            if (targetCard) {
                targetCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    });

    // Initial state
    updateMap(null);
});