function switchTab(name) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-button').forEach(el => el.classList.remove('active'));
    document.getElementById(name).classList.add('active');
    event.target.classList.add('active');
}

document.getElementById('embedForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const status = document.getElementById('embedStatus');
    status.textContent = 'Embedding...';
    status.className = 'status';

    const formData = new FormData(e.target);
    try {
        const res = await fetch('/api/embed', { method: 'POST', body: formData });
        if (res.ok) {
            const blob = await res.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'stego_output.png';
            a.click();
            status.textContent = '✅ Message embedded — file downloaded.';
            status.className = 'status success';
        } else {
            const data = await res.json();
            status.textContent = `❌ ${data.error}`;
            status.className = 'status error';
        }
    } catch {
        status.textContent = '❌ Network error.';
        status.className = 'status error';
    }
});

document.getElementById('extractForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const status = document.getElementById('extractStatus');
    const resultBox = document.getElementById('extractResult');
    status.textContent = 'Extracting...';
    status.className = 'status';
    resultBox.style.display = 'none';

    const formData = new FormData(e.target);
    try {
        const res = await fetch('/api/extract', { method: 'POST', body: formData });
        const data = await res.json();
        if (res.ok && data.success) {
            document.getElementById('resultText').value = data.message;
            resultBox.style.display = 'block';
            status.textContent = '✅ Message extracted successfully.';
            status.className = 'status success';
        } else {
            status.textContent = `❌ ${data.error}`;
            status.className = 'status error';
        }
    } catch {
        status.textContent = '❌ Network error.';
        status.className = 'status error';
    }
});
