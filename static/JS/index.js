const header = document.getElementById('header')


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