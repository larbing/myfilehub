function handleFileUpload(files,progress,uploadMessage) {

    var formData = new FormData();
    for (var i = 0; i < files.length; i++) {
        formData.append('files[]', files[i]);
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload'); // 替换为你的上传端点
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


function showUploadOverlay() {
    // var files = event.target.files;
    // if (files.length === 0) {
    //     alert("请至少选择一个文件!");
    //     return;
    // }

    var overlay = document.getElementById('popupUploadWindow');
    overlay.style.display = 'flex';

    // var progress = document.getElementById('uploadProgress');
    // progress.value = 0;

    // handleFileUpload(files,progress,overlay);
}




