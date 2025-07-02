document.addEventListener('DOMContentLoaded', function() {
    // Footer year update
    const footerYear = document.getElementById("footer-year");
    if (footerYear) {
        footerYear.textContent = new Date().getFullYear();
    }

    // Document upload form handling
    const form = document.getElementById('uploadForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const fileInput = document.getElementById('document');
            const formData = new FormData();
            formData.append('document', fileInput.files[0]);
            const resultDiv = document.getElementById('analysisResult');
            resultDiv.innerHTML = 'Analyzing...';
            fetch('/analyze', {
                method: 'POST',
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    resultDiv.innerHTML = `<span style="color: red;">Error: ${data.error}</span>`;
                } else {
                    let html = `<strong>Risk Score:</strong> ${data.risk_score}%<br><strong>Highlights:</strong><ul>`;
                    data.highlights.forEach(line => {
                        html += `<li>${line}</li>`;
                    });
                    html += '</ul>';
                    resultDiv.innerHTML = html;
                }
            }).catch(() => {
                resultDiv.innerHTML = "<span style='color:red;'>Analysis failed. Please try again.</span>";
            });
        });
    }
});