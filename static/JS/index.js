const header = document.getElementById('header')
const footer = document.getElementById('footer')

header.innerHTML = `
        <div class="nav-container">
            <button id="mobileToggle" class="mobile-toggle"><span></span></button>
            <div id="mobileMenu" class="mobile-menu">
                <!-- your menu items here -->
            </div>
            ${home}
            
            <nav>
                <ul class="nav-links mobile-elements-nav" id="navLinks" >
                    ${nav_urls}
                </ul>
            </nav>
            <div class="search-container" style="display:none;">
                ${search}
            </div>

            ${login}            

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
    const time = Math.ceil(diffTime / (1000));
    let result = ''

    if(time < 60){
        result = "few seconds ago";
    }

    else if(time < 3600){
        if (Math.ceil(time/60) == 1){
            result = `a minute ago`;
        }
        else{
            result = `${time/60} minutes ago`;
        }
        
        }

    else if(time < (3600 * 24)){
        result = `${Math.ceil(time/(3600))} hours ago`;
    }
        
    else if(time < (3600 * 24 * 30)){ //current month
        result = `${Math.ceil(time/(3600 * 24))} days ago`;
        }
    
    else if(time < (3600 * 24 * 30 * 12)){
        result = `${Math.ceil(time/(3600 * 24 * 30))} months ago`
    }
        
    else{
        result = `${Math.ceil(time/(3600 * 24 * 30 * 12))} years ago`
    }
    
    return result
}

dateELems = document.getElementsByClassName('datetime')
console.log(dateELems)
for(i=0; i<dateELems.length; i++) {
    let dateElem = dateELems[i]
    console.log(dateElem.textContent)
    dateElem.textContent = formatDate(dateElem.textContent)
};

//mobile friendly
const mobileToggle = document.getElementById("mobileToggle");
const mobileMenu = document.getElementById("mobileMenu");
const navElements = document.getElementById('navLinks')
const Avatar = document.getElementsByClassName('user-avatar');
const dropDownElements = document.getElementsByClassName('dropdown-menu');

/*
//add to mobile menu
if (window.innerWidth <= 768) {
    Array.from(navElements.children).forEach(element => {
      mobileMenu.appendChild(element)  
    });    
}

if (window.innerWidth > 768){
    Array.from(navElements.children).forEach(element => {
      mobileMenu.appendChild(element)  
    }); 
}


// Toggle Mobile Menu
mobileMenu.style.display = 'none'
mobileToggle.addEventListener("click", () => {
    if(mobileToggle.className == 'mobile-toggle'){
        mobileToggle.className = 'mobile-toggle-active'
        mobileMenu.style.display = 'block'
        mobileMenu.style.left = '0'



    }
    else{
        mobileToggle.className = 'mobile-toggle'
        mobileMenu.style.display = 'none'
        mobileMenu.style.left = '-50%'

    }
});
*/