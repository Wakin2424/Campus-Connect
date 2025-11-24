const header = document.getElementById('header')
const footer = document.getElementById('footer')

header.innerHTML = `
        <div class="nav-container">
            ${home}
            
            <nav>
                <ul class="nav-links" id="navLinks">
                    ${nav_urls}
                </ul>
            </nav>
            <div class="search-container">
                ${search}
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


function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}


dateELems = document.getElementsByClassName('date-upload')
console.log(dateELems)
for(i=0; i<dateELems.length; i++) {
    let dateElem = dateELems[i]
    console.log(dateElem.textContent)
    dateElem.textContent = formatDate(dateElem.textContent)
};