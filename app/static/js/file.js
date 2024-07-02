function handleFileUpload(files,progress,overlay) {

    var formData = new FormData();
    for (var i = 0; i < files.length; i++) {
        formData.append('files[]', files[i]);
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload'); // 替换为你的上传端点
    xhr.upload.onprogress = function(e) {
        if (e.lengthComputable) {
            var percentComplete = e.loaded / e.total * 100;
            progress.value = percentComplete;
        }
    };
    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 400) {
            // 成功上传
            alert('文件上传成功！');
        } else {
            // 处理上传失败的情况
            alert('文件上传失败，请检查网络连接!');
        }
        overlay.style.display = 'none';
    };
    xhr.onerror = function() {
        alert('文件上传失败，请检查网络连接!');
        overlay.style.display = 'none';
    };
    xhr.send(formData);
}


function showUploadOverlay(event) {
    var files = event.target.files;
    if (files.length === 0) {
        alert("请至少选择一个文件!");
        return;
    }

    var overlay = document.getElementById('uploadOverlay');
    overlay.style.display = 'flex';

    var progress = document.getElementById('uploadProgress');
    progress.value = 0;

    // 假设这是上传文件的函数
    handleFileUpload(files,progress,overlay);
    // uploadFiles(files).then(function() {
    //     overlay.style.display = 'none';
    //     alert('文件上传成功！');
    // }).catch(function() {
    //     overlay.style.display = 'none';
    //     alert('文件上传失败，请检查网络连接!');
    // });
}

// 这里应该是你的上传文件的函数
async function uploadFiles(files) {
    // 模拟上传过程
    for (var i = 0; i <= 100; i += 10) {
        await new Promise(resolve => setTimeout(resolve, 500));
        document.getElementById('uploadProgress').value = i;
    }
    return true;
}

