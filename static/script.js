document.getElementById('upload-button').addEventListener('click', () => {
    document.getElementById('file-upload').click();
});

document.getElementById('file-upload').addEventListener('change', async function() {
    const file = this.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                const downloadLink = document.getElementById('download-link');
                downloadLink.href = `/download/${data.file}`;
                document.getElementById('download-section').style.display = 'block';
            } else {
                alert('Failed to upload file');
            }
        } catch (error) {
            console.error('Error uploading file:', error);
            alert('An error occurred while uploading the file');
        }
    }
});
