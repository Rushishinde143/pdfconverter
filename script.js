document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData();
    const files = document.getElementById('images').files;
    const layout = document.getElementById('layout').value;

    for (let i = 0; i < files.length; i++) {
        formData.append('images', files[i]);
    }
    formData.append('layout', layout);

    try {
        const response = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            document.getElementById('message').innerText = error.error;
            return;
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'converted.pdf';
        document.body.appendChild(a);
        a.click();
        a.remove();
    } catch (err) {
        document.getElementById('message').innerText = 'An error occurred while uploading.';
    }
});
