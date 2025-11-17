document.addEventListener('DOMContentLoaded', () => {
    const newsContainer = document.getElementById('news-container');
    const loadingIndicator = document.getElementById('loading');
    const refreshBtn = document.getElementById('refreshBtn');

    // --- CONFIGURATION ---
    // Replace this with your actual Render backend URL
    const API_BASE_URL = 'YOUR_RENDER_BACKEND_URL_HERE'; 

    const showLoading = (show) => {
        loadingIndicator.style.display = show ? 'block' : 'none';
    };

    const fetchNews = async () => {
        showLoading(true);
        newsContainer.innerHTML = ''; // Clear existing news

        if (API_BASE_URL === 'YOUR_RENDER_BACKEND_URL_HERE') {
            showError("Please update the `API_BASE_URL` in `frontend/js/app.js` with your backend URL.");
            showLoading(false);
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/news?limit=50`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const articles = await response.json();
            renderArticles(articles);
        } catch (error) {
            console.error("Failed to fetch news:", error);
            showError("Could not load news. Is the backend running?");
        } finally {
            showLoading(false);
        }
    };

    const renderArticles = (articles) => {
        if (!articles || articles.length === 0) {
            newsContainer.innerHTML = '<p class="text-center">No news articles found. Try refreshing later.</p>';
            return;
        }

        articles.forEach(article => {
            const articleElement = document.createElement('div');
            articleElement.className = 'col-md-6 col-lg-4';
            
            const sentimentScore = article.sentiment ? article.sentiment.score.toFixed(2) : 'N/A';
            const sentimentLabel = article.sentiment ? article.sentiment.label : 'N/A';
            const sentimentBadgeClass = sentimentLabel === 'POSITIVE' ? 'bg-success' : 'bg-danger';

            articleElement.innerHTML = `
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">${article.title}</h5>
                        <h6 class="card-subtitle mb-2 text-muted">${article.source} - ${new Date(article.published_date).toLocaleDateString()}</h6>
                        <p class="card-text">${article.summary || 'No summary available.'}</p>
                    </div>
                    <div class="card-footer d-flex justify-content-between align-items-center">
                        <div>
                            <span class="badge bg-primary me-1">${article.category || 'General'}</span>
                            <span class="badge ${sentimentBadgeClass}">${sentimentLabel} (${sentimentScore})</span>
                        </div>
                        <a href="${article.url}" target="_blank" class="btn btn-sm btn-outline-secondary">Read More</a>
                    </div>
                </div>
            `;
            newsContainer.appendChild(articleElement);
        });
    };

    const showError = (message) => {
        newsContainer.innerHTML = `<div class="alert alert-danger w-100">${message}</div>`;
    }

    const handleRefresh = async () => {
        if (API_BASE_URL === 'YOUR_RENDER_BACKEND_URL_HERE') {
            alert("Please set your backend URL in js/app.js first.");
            return;
        }
        
        refreshBtn.disabled = true;
        refreshBtn.textContent = 'Refreshing...';

        try {
            await fetch(`${API_BASE_URL}/refresh_news`, { method: 'POST' });
            alert('News refresh triggered! It may take a few minutes for new articles to appear. Please refresh the page later.');
        } catch (error) {
            console.error('Failed to trigger refresh:', error);
            alert('Failed to trigger refresh. Check the console for details.');
        } finally {
            refreshBtn.disabled = false;
            refreshBtn.textContent = 'Refresh News';
        }
    };

    // Initial load
    fetchNews();

    // Event Listeners
    refreshBtn.addEventListener('click', handleRefresh);
});
