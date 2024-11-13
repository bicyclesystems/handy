function handleBrTags() {
    const isMobile = window.innerWidth <= 768; 
    document.querySelectorAll('br').forEach(function(br) {
        if (isMobile) {
            br.style.display = 'none';
        } else {
            br.style.display = ''; 
        }
    });

    const videoElement = document.getElementById('motion-video');
    if (videoElement) {
        if (isMobile) {
            videoElement.style.transform = 'scale(1.3)'; 
        } else {
            videoElement.style.transform = ''; 
        }
    }
}

handleBrTags();

window.addEventListener('resize', handleBrTags);