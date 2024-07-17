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
        this.updateFileTextButton = this.$('updateFileTextButton');
        this.fileId = this.$('fileId');
        this.init();
    }

    init() {
        this.closeWindowButton.addEventListener('click', this.closeWindowHandle.bind(this));
        this.updateFileTextButton.addEventListener('click', this.updateFileTextHandle.bind(this));
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

    openTextWindow(fileId, filename) {
        const url = "/share/" + fileId + "/name/" + filename;
        this.popupWindow.style.display = 'flex';
        this.fileText.style.display = 'flex';
        this.updateFileTextButton.style.display = 'flex';
        this.fileId.value = fileId;

        fetch(url, {
            headers: {
                'content-bytes-limit': 1048576
            }
        })
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

    updateFileTextHandle() {
        const url = "/update-context";

        const data = {
            "fileId": this.fileId.value,
            "context": this.fileText.value
        };

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(text => {
                alert(text);
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