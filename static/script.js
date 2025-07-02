// Get references to elements
const sidebar = document.getElementById('sidebar'); // Added sidebar element
const sidebarTriggerArea = document.getElementById('sidebar-trigger-area'); // Added trigger area
const navLinks = document.querySelectorAll('aside nav ul li a');
const sections = document.querySelectorAll('main section');

// Define the threshold for showing the sidebar (e.g., 20px from the left edge)
const triggerThreshold = 20;
// Define the buffer area to hide the sidebar (e.g., sidebar width + 10px)
let hideThreshold; // Will be initialized on DOMContentLoaded

// Function to show the sidebar
function showSidebar() {
    sidebar.classList.add('sidebar-open');
}

// Function to hide the sidebar
function hideSidebar() {
    sidebar.classList.remove('sidebar-open');
}

// Mousemove event listener for the entire document
document.addEventListener('mousemove', (e) => {
    // If mouse is near the left edge and sidebar is hidden, show it
    if (e.clientX < triggerThreshold && !sidebar.classList.contains('sidebar-open')) {
        showSidebar();
    }
    // If mouse moves out of the sidebar area and sidebar is open, hide it
    // Ensure hideThreshold is defined before using it
    else if (hideThreshold && e.clientX > hideThreshold && sidebar.classList.contains('sidebar-open')) {
        hideSidebar();
    }
});

// Add event listener to sidebar itself to keep it open when mouse is over it
sidebar.addEventListener('mouseleave', (e) => {
    // Hide sidebar only if mouse leaves the sidebar and is not immediately re-entering the trigger area
    // Check if mouse is outside the sidebar's visual boundary
    if (e.clientX > sidebar.offsetWidth) {
        hideSidebar();
    }
});


// Function to remove 'active' class from all links
function removeAllActiveClasses() {
    navLinks.forEach(link => {
        link.classList.remove('active');
    });
}

// Function to add 'active' class to the current link
function setActiveLink(targetId) {
    removeAllActiveClasses();
    // Select the link using its href attribute to ensure correct targeting
    const activeLink = document.querySelector(`a.sidebar-link[href="${targetId}"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }
}

// Add click event listener to each link for smooth scrolling and active class
navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent default anchor link behavior

        const targetId = this.getAttribute('href'); // Get the href attribute (e.g., "#dashboard-section")
        const targetElement = document.querySelector(targetId); // Find the element with that ID

        if (targetElement) {
            // Scroll smoothly to the target element
            targetElement.scrollIntoView({
                behavior: 'smooth'
            });
            // Set active class immediately on click
            setActiveLink(targetId);
        }
    });
});

// Intersection Observer to highlight active link on scroll
// This observes when a section enters or exits the viewport
const observerOptions = {
    root: null, // viewport as the root
    rootMargin: '0px',
    threshold: 0.3 // 30% of the section must be visible to be considered 'intersecting'
};

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            // If a section is intersecting, set its corresponding link as active
            const sectionId = `#${entry.target.id}`;
            setActiveLink(sectionId);
        }
    });
}, observerOptions);

// Observe each section to detect when it enters the viewport
sections.forEach(section => {
    observer.observe(section);
});

// Set initial active link on page load (for the first visible section)
document.addEventListener('DOMContentLoaded', () => {
    // Initialize hideThreshold here, after the DOM is loaded and sidebar width is available
    hideThreshold = sidebar.offsetWidth + 10;

    // Loop through sections to find the first one that is currently visible in the viewport
    for (let i = 0; i < sections.length; i++) {
        const rect = sections[i].getBoundingClientRect();
        // Check if the top of the section is within the viewport
        if (rect.top >= 0 && rect.top <= window.innerHeight) {
            setActiveLink(`#${sections[i].id}`);
            break; // Stop after finding the first visible section
        }
    }
});

// Ensure hideThreshold is updated if the sidebar width changes (e.g., window resize)
window.addEventListener('resize', () => {
    hideThreshold = sidebar.offsetWidth + 10;
});
