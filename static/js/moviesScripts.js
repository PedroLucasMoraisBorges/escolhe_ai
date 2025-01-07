document.addEventListener("DOMContentLoaded", function () {
    // Filtro de filmes por título
    const searchInput = document.querySelector("#search-movies");
    const tableRows = document.querySelectorAll(".movie-table tbody tr");

    if (searchInput) {
        searchInput.addEventListener("input", function () {
            const query = searchInput.value.toLowerCase();
            tableRows.forEach(row => {
                const title = row.querySelector("td:nth-child(3) a").textContent.toLowerCase();
                row.style.display = title.includes(query) ? "" : "none";
            });
        });
    }

    // Classificar filmes por classificação
    const ratingHeader = document.querySelector(".movie-table th:nth-child(5)");
    if (ratingHeader) {
        ratingHeader.addEventListener("click", function () {
            const rows = Array.from(tableRows);
            const sortedRows = rows.sort((a, b) => {
                const ratingA = parseFloat(a.querySelector("td:nth-child(5)").textContent) || 0;
                const ratingB = parseFloat(b.querySelector("td:nth-child(5)").textContent) || 0;
                return ratingB - ratingA; // Ordem decrescente
            });
            const tbody = document.querySelector(".movie-table tbody");
            tbody.innerHTML = ""; // Limpa as linhas
            sortedRows.forEach(row => tbody.appendChild(row)); // Reanexa em ordem
        });
    }
});
