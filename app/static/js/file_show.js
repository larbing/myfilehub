class FileShower {

    constructor() {
        this.$ = function (id) {
            return document.getElementById(id);
        }

        this.popupWindow = this.$('popupImageWindow');
        this.closeWindowButton = this.$('closeImageWindowButton');
        this.fileImage = this.$('fileImage');
        this.fileVideo = this.$('fileVideo');
        this.fileText = this.$('fileText');
        this.init();
    }

    init() {
        this.closeWindowButton.addEventListener('click', this.closeWindowHandle.bind(this));
    }

    openImageWindow(url) {
        this.popupWindow.style.display = 'flex';
        this.fileImage.style.display = 'flex';
        this.fileImage.src = url;
    }

    openVideoWindow(url) {
        this.popupWindow.style.display = 'flex';
        this.fileVideo.style.display = 'flex';
        this.fileVideo.src = url;
    }

    openTextWindow(url) {
        this.popupWindow.style.display = 'flex';
        this.fileText.style.display = 'flex';

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(text => {
                this.fileText.value = text;
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });

    }

    closeWindowHandle(e) {
        this.popupWindow.style.display = 'none';
        this.fileImage.style.display = 'none';
        this.fileVideo.style.display = 'none';
        this.fileVideo.pause();
        this.fileText.style.display = 'none';
        this.fileText.value = '';
    }

}