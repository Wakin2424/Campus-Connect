const header = document.getElementById('header')
const footer = document.getElementById('footer')

// Sticky navbar on scroll
window.addEventListener('scroll', function() {
    const header = document.getElementById('header');
    if (window.scrollY > 100) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Mobile menu toggle
const mobileToggle = document.getElementById('mobileToggle');
const navLinks = document.getElementById('navLinks');

mobileToggle.addEventListener('click', function() {
    navLinks.classList.toggle('active');
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Close mobile menu when clicking on a link
navLinks.addEventListener('click', function(e) {
    if (e.target.tagName === 'A') {
        navLinks.classList.remove('active');
    }
});


const searchBar = document.querySelector('.search-bar');
searchBar.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        alert('Search functionality would be implemented here!');
    }
});

function Search(){
    //let url = search_btn.url
    console.log('hello')
}


header.innerHTML = `
        <div class="nav-container">
            ${home}
            
            <nav>
                <ul class="nav-links" id="navLinks">
                    ${nav_urls}
                </ul>
            </nav>
            <div class="search-container">
                <input type="text" id='search-bar' class="search-bar" placeholder="Search...">
                <button class="search-btn" id='search-btn' onClick='Search()'>🔍</button>    
            </div>

            ${login}
                      

            <div class="mobile-toggle" id="mobileToggle">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
`

footer.innerHTML = `
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Quick Links</h3>
                    ${footer_urls}
                </div>

                <div class="footer-section">
                    <h3>Features</h3>
                    ${footer_urls_2}
                </div>

                <div class="footer-section">
                    <h3>Community</h3>
                    <a href="#">Guidelines</a>
                    <a href="#">Safety Tips</a>
                    <a href="#">Success Stories</a>
                    <a href="#">Campus Partners</a>
                    <a href="#">Student Resources</a>
                </div>

                <div class="footer-section">
                    <h3>Connect With Us</h3>
                    <p>Join thousands of students already connecting on Campus Connect.</p>
                    <div class="social-icons">
                        <a href="#"><i class="fab fa-facebook-f"></i></a>
                        <a href="#"><i class="fab fa-twitter"></i></a>
                        <a href="#"><i class="fab fa-instagram"></i></a>
                        <a href="#"><i class="fab fa-linkedin-in"></i></a>
                    </div>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>&copy; 2025 Campus Connect. All rights reserved. Made with ❤️ for students.</p>
            </div>
        </div>
`

