// S'assurer que le code s'exécute après le chargement du DOM
document.addEventListener('DOMContentLoaded', function() {
    // Vérifier que le canvas existe
    const canvas = document.getElementById("chartjs-doughnut");
    if (canvas) {
        new Chart(canvas, {
            type: "doughnut",
            data: {
                labels: ["Social", "Search Engines", "Direct", "Other"],
                datasets: [{
                    data: [260, 125, 54, 146],
                    backgroundColor: [
                        window.theme?.primary || "#4e73df",
                        window.theme?.success || "#1cc88a",
                        window.theme?.warning || "#f6c23e",
                        "#dee2e6"
                    ],
                    borderColor: "transparent"
                }]
            },
            options: {
                maintainAspectRatio: false,
                cutoutPercentage: 65,
            }
        });
    }
});