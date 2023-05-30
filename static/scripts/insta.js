function shareToInstagram() {
    // get current URL
    const currentPageUrl = window.location.href;

    // get share button
    const shareButton = document.getElementById('instagram-share');

    // add event listener of share button
    shareButton.addEventListener('click', function() {
        // get share url
        const instagramUrl = 'https://www.instagram.com/sharer.php?u=' + encodeURIComponent(currentPageUrl);

        // create new window
        const newWindow = window.open(instagramUrl, '_blank');

        // check if the new window is opened
        if (!newWindow || newWindow.closed || typeof newWindow.closed === 'undefined') {
            // if not then show the error message
            alert('Failed to open Instagram page. Please try again.');
          }
    })}
