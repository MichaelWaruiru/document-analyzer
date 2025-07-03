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
            const progressContainer = document.getElementById('progressContainer');
            const progressBar = document.getElementById('progressBar');

            // Reset and show progress bar
            progressBar.style.width = '0%';
            progressBar.setAttribute('aria-valuenow', 0);
            progressBar.textContent = '0%';
            progressContainer.style.display = 'block';
            resultDiv.innerHTML = '';

            // Simulate progress bar animation
            let progress = 0;
            let fakeInterval = setInterval(() => {
                progress += Math.random() * 12 + 5; // Increment randomly for realism
                if (progress >= 100) progress = 98; // Keep under 100 until fetch completes
                progressBar.style.width = progress + '%';
                progressBar.setAttribute('aria-valuenow', Math.floor(progress));
                progressBar.textContent = Math.floor(progress) + '%';
            }, 250);

            fetch('/analyze', {
                method: 'POST',
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                clearInterval(fakeInterval);
                progressBar.style.width = '100%';
                progressBar.setAttribute('aria-valuenow', 100);
                progressBar.textContent = '100%';
                setTimeout(() => {
                    progressContainer.style.display = 'none';
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
                }, 400); // Short pause for effect
            }).catch(() => {
                clearInterval(fakeInterval);
                progressBar.style.width = '100%';
                progressBar.setAttribute('aria-valuenow', 100);
                progressBar.textContent = '100%';
                setTimeout(() => {
                    progressContainer.style.display = 'none';
                    resultDiv.innerHTML = "<span style='color:red;'>Analysis failed. Please try again.</span>";
                }, 400);
            });
        });
    }

    // Highlight Modal handling for dashboard.html
    var highlightModal = document.getElementById('highlightModal');
    if (highlightModal) {
        highlightModal.addEventListener('show.bs.modal', function (event) {
            var button = event.relatedTarget;
            var highlights = button.getAttribute('data-highlights') || '';
            var filename = button.getAttribute('data-filename') || '';
            var modalHighlights = highlightModal.querySelector('#modalHighlights');
            var modalFilename = highlightModal.querySelector('#modalFilename');
            modalFilename.textContent = filename;

            // Convert HTML entity for line break (&#10;) back to real \n
            highlights = highlights.replace(/&#10;/g, '\n');
            var lines = highlights.split('\n').filter(line => line.trim() !== "");
            if (lines.length) {
                modalHighlights.innerHTML = '<ul>' + lines.map(function(line) {
                    return '<li class="text-muted small">' + line + '</li>';
                }).join('') + '</ul>';
            } else {
                modalHighlights.innerHTML = "<span class='text-muted small'>No highlights available.</span>";
            }
        });
    }
});

// Password visibility toggle function (global, so can be called from inline HTML)
function togglePassword(fieldId, iconSpan) {
    var input = document.getElementById(fieldId);
    var icon = iconSpan.querySelector('i');
    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        input.type = "password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }
}