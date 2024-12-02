function handleBrTags() {
    const isMobile = window.innerWidth <= 768;
    
    document.querySelectorAll('br').forEach(function(br) {
        br.style.display = isMobile ? 'none' : '';
    });
    
    const videoElement = document.getElementById('motion-video');
    if (videoElement) {
        videoElement.style.transform = isMobile ? 'scale(1.3)' : '';
    }
    
    document.querySelectorAll('.preorder, .dollar').forEach(element => {
        if (isMobile) {
            element.style.left = '0';
            element.style.right = '0';
        } else {
            if (element.classList.contains('preorder')) {
                element.style.right = '-5%';
                element.style.left = '';
            } else {
                element.style.left = '-5%';
                element.style.right = '';
            }
        }
    });

    if (isMobile) {
        document.querySelectorAll('.hemi').forEach(element => {
            element.style.height = '140%';
        });
        
        document.querySelectorAll('.hand-image').forEach(element => {
            element.style.width = '85%';
        });

        document.querySelectorAll('.pre-order').forEach(element => {
            element.classList.remove('gap-xl');
            element.classList.add('gap-m');
        });
    } else {
        document.querySelectorAll('.hemi').forEach(element => {
            element.style.height = '';
        });
        
        document.querySelectorAll('.hand-image').forEach(element => {
            element.style.width = '40%';
        });

        document.querySelectorAll('.pre-order').forEach(element => {
            element.classList.remove('gap-m');
            element.classList.add('gap-xl');
        });
    }
}

handleBrTags();
window.addEventListener('resize', handleBrTags);