document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);

    fetch('/pma_checker', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            renderResults(data.success_results, data.error_results);
        }
    })
    .catch(error => console.error('Error:', error));
});

function renderResults(successResults, errorResults) {
    let resultsContainer = document.getElementById('resultsContainer');
    let html = '';

    if (successResults.length > 0 || errorResults.length > 0) {
        html += `<h3>Results</h3>
                 <table>
                     <thead>
                         <tr>
                             <th>Result</th>
                             <th>Country Flag</th>
                             <th>Auto Login Link</th>
                             <th>Host</th>
                             <th>DB Username</th>
                             <th>DB Password</th>
                             <th>Database</th>
                         </tr>
                     </thead>
                     <tbody>`;

        successResults.forEach(result => {
            html += `<tr>
                        <td><span class="success">${result.Result}</span></td>
                        <td>${result.CountryFlag}</td>
                        <td><a href="${result.Auto_Login_Link}" target="_blank">${result.Auto_Login_Link}</a></td>
                        <td>${result.DB_HOST}</td>
                        <td>${result.DB_USERNAME}</td>
                        <td>${result.DB_PASSWORD}</td>
                        <td>${result.DB_DATABASE}</td>
                    </tr>`;
        });

        errorResults.forEach(result => {
            html += `<tr>
                        <td><span class="error">${result.error}</span></td>
                        <td>${result.entry.DBS_COUNTRY}</td>
                        <td>${result.entry.DB_HOST}</td>
                        <td>${result.entry.DB_USERNAME}</td>
                        <td>${result.entry.DB_PASSWORD}</td>
                        <td>${result.entry.DB_DATABASE}</td>
                    </tr>`;
        });

        html += `</tbody>
                 </table>
                 <div class="download-buttons">
                     <button onclick="downloadResults('json')">Download JSON</button>
                     <button onclick="downloadResults('text')">Download Text</button>
                     <button onclick="downloadResults('csv')">Download CSV</button>
                     <button onclick="downloadResults('html')">Download HTML</button>
                 </div>`;
    } else {
        html += '<p>No results found.</p>';
    }

    resultsContainer.innerHTML = html;
}

function downloadResults(format) {
    const url = `/download/${format}`;
    window.location.href = url;
}

// Fetch existing results on page load
window.addEventListener('DOMContentLoaded', (event) => {
    fetch('/pma_checker')
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            renderResults(data.success_results, data.error_results);
        }
    })
    .catch(error => console.error('Error:', error));
});
