document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('uploadForm');
    const urlInput = document.getElementById('url');
    const fileInput = document.getElementById('file');
    const dropArea = document.getElementById('dropArea');
    const output = document.getElementById('output');

    // Add URL validation function
    function isValidGovUrl(url) {
        try {
            let urlToCheck = url;
            // If no protocol is specified, prepend https://
            if (!url.startsWith('http://') && !url.startsWith('https://')) {
                urlToCheck = 'https://' + url;
            }
            const urlObj = new URL(urlToCheck);
            // Updated regex to accept both .gov and .gov.XX domains
            const govDomainRegex = /^([a-zA-Z0-9-]+\.)*(gov|gob)(\.[a-z]{2,6})?$/i;
            return govDomainRegex.test(urlObj.hostname);
        } catch {
            return false;
        }
    }

    // Add input validation
    urlInput.addEventListener('input', (e) => {
        const url = e.target.value;
        if (url && !isValidGovUrl(url)) {
            urlInput.setCustomValidity('Please enter a valid government URL (e.g., https://data.seattle.gov/dataset/example, https://www.economia.gob.mx/path)');
        } else {
            urlInput.setCustomValidity('');
        }
    });


    // Handle drag and drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropArea.classList.add('drag-over');
    }

    function unhighlight() {
        dropArea.classList.remove('drag-over');
    }

    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        fileInput.files = files;
        updateFileName();
    }

    // Handle file selection
    dropArea.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', updateFileName);

    function updateFileName() {
        const fileName = fileInput.files[0] ? fileInput.files[0].name : '';
        dropArea.innerHTML = fileName
            ? `<p>Selected file: ${fileName}</p>`
            : '<p>Drag and drop your file here, or click to select</p>';
    }

    // Handle form submission
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const url = urlInput.value;
        const file = fileInput.files[0];
        
        if (!isValidGovUrl(url)) {
            output.textContent = 'Error: Invalid government URL';
            return;
        }
        
        output.textContent = `URL: ${url}\nFile: ${file ? file.name : 'No file uploaded'}`;
    });

});