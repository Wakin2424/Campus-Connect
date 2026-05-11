const header = document.getElementById('header')


header.innerHTML = `
        <div class="nav-container">
            <button id="mobileToggle" class="mobile-toggle">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <div id="mobileMenu" class="mobile-menu">
                <!-- your menu items here -->
            </div>
            ${home}
            
            <nav>
                <ul class="nav-links mobile-elements-nav" id="navLinks" >
                    ${nav_urls}
                </ul>
            </nav>
            <div class="search-container">
                ${search}
            </div>

            ${login}            

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
            result = `${Math.round(time/60)} minutes ago`;
        }
        
        }

    else if(time < (3600 * 24)){
        result = `${Math.round(Math.ceil(time/(3600)))} hours ago`;
    }
        
    else if(time < (3600 * 24 * 30)){ //current month
        result = `${Math.round(Math.ceil(time/(3600 * 24)))} days ago`;
        }
    
    else if(time < (3600 * 24 * 30 * 12)){
        result = `${Math.round(Math.ceil(time/(3600 * 24 * 30)))} months ago`
    }
        
    else if(time > (3600 * 24 * 30 * 12)){
        result = `${Math.round(Math.ceil(time/(3600 * 24 * 30 * 12)))} years ago`
    }

    else{
        result = `some time ago`
    }
    
    return result
}

function Search(){
    let searchInput = document.getElementById('search-bar')
    let result = searchInput.value
    let url = searchInput.dataset.url
    window.location.href = `${url}?result=${result}`
}

dateELems = document.getElementsByClassName('datetime')
for(i=0; i<dateELems.length; i++) {
    let dateElem = dateELems[i]
    console.log(dateElem.textContent)
    dateElem.textContent = formatDate(dateElem.textContent)
};

// ==========================
// MOBILE NAVIGATION
// ==========================

// ==========================
// MOBILE NAVIGATION
// ==========================

const mobileToggle = document.getElementById("mobileToggle");
const mobileMenu = document.getElementById("mobileMenu");
const navLinks = document.getElementById("navLinks");

// Create mobile nav dynamically
mobileMenu.innerHTML = `
    <ul>
        ${nav_urls}
        <li><a href="/user/">Profile</a></li>
        <li><a href="/auth/logout">Logout</a></li>
    </ul>
`;

// Toggle menu
mobileToggle.addEventListener("click", () => {

    mobileToggle.classList.toggle("active");
    mobileMenu.classList.toggle("active");

});

// Close menu when clicking a link
document.querySelectorAll(".mobile-menu a").forEach(link => {

    link.addEventListener("click", () => {
        mobileToggle.classList.remove("active");
        mobileMenu.classList.remove("active");
    });

});