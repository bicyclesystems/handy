function handleBrTags() {
    const isMobile = window.innerWidth <= 768; 
    document.querySelectorAll('br').forEach(function(br) {
        if (isMobile) {
            br.style.display = 'none';
        } else {
            br.style.display = ''; 
        }
    });
}

handleBrTags();

window.addEventListener('resize', handleBrTags);