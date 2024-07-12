class FileUploader {
    constructor() {
        this.dropArea = document.getElementById('dropArea');
        this.fileInput = document.getElementById('fileUpload');
        this.progress = document.getElementById('uploadProgress');
        this.uploadMessage = document.getElementById('uploadMessage');
        this.uploadFilePopup = document.getElementById('popupUploadWindow');
        this.closeUploadWindow = document.getElementById('closeUploadWindow');
        this.uploadFileButton = document.getElementById('uploadFileButton');
        this.init();
    }

    init() {
        this.dropArea.addEventListener('click', this.handleClick.bind(this));
        this.dropArea.addEventListener('dragenter', this.handleDragEnter.bind(this));
        this.dropArea.addEventListener('dragleave', this.handleDragLeave.bind(this));
        this.dropArea.addEventListener('dragover', this.handleDragOver.bind(this));
        this.dropArea.addEventListener('drop', this.handleDrop.bind(this));

        this.closeUploadWindow.addEventListener('click', this.handleCloseWindow.bind(this));
        this.uploadFileButton.addEventListener('click', this.handleOpenUploadWindow.bind(this));
    }

    handleOpenUploadWindow() {
        this.uploadFilePopup.style.display = 'flex';
        this.uploadMessage.innerText = '';
        this.progress.value = 0;
        this.progress.max = 100;
        this.progress.style.display = 'none';
    }

    handleCloseWindow(e) {
        this.uploadFilePopup.style.display = 'none';
    }

    handleClick(e) {
        this.fileInput.addEventListener('change', this.handleFileChange.bind(this));
        this.fileInput.click();
    }

    handleFileChange(e) {
        const files = e.target.files;
        if (files.length === 0) {
            alert("请至少选择一个文件!");
            return;
        }
        this.handleFiles(files);
    }

    handleDragEnter(e) {
        e.stopPropagation();
        e.preventDefault();
        e.dataTransfer.dropEffect = 'copy';
        this.dropArea.classList.add('dragover');
    }

    handleDragLeave(e) {
        e.stopPropagation();
        e.preventDefault();
        this.dropArea.classList.remove('dragover');
    }

    handleDragOver(e) {
        e.stopPropagation();
        e.preventDefault();
    }

    handleDrop(e) {
        e.stopPropagation();
        e.preventDefault();
        const files = e.dataTransfer.files;
        this.handleFiles(files);
        this.dropArea.classList.remove('dragover');
    }

    handleFiles(files) {
        this.progress.value = 0;
        this.progress.style.display = 'flex';
        this.uploadMessage.innerText = '正在上传...';
        this.uploadFiles(files);
    }

    uploadFiles(files) {

        const formData = new FormData();
        for (var i = 0; i < files.length; i++) {
            formData.append('files[]', files[i]);
        }
        
        const progress = this.progress;
        const uploadMessage = this.uploadMessage;
        
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/upload'); 

        xhr.upload.onprogress = function(e) {
            if (e.lengthComputable) {
                progress.max = e.total;
                progress.value = e.loaded;
            }
        };
    
        xhr.onload = function() {
            if (xhr.status >= 200 && xhr.status < 400) {
                // 成功上传
                uploadMessage.innerText =  '文件上传成功！';
            } else {
                // 处理上传失败的情况
                uploadMessage.innerText = '文件上传失败，请检查网络连接!';
            }
        };

        xhr.onerror = function() {
            uploadMessage.innerText = '文件上传失败，请检查网络连接!';
        };

        xhr.send(formData);
    }
}
