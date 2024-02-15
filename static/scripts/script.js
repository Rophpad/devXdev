import { jsPDF } from "jspdf";

window.onload = function() {
    const downloadBtn = document.getElementById("download-pdf");

    downloadBtn.addEventListener("click", () => {
      console.log('HEllo');
      const doc = new jsPDF();

  // Get div element containing stats
        const statsEl = document.getElementById("github-stats");

  // Define page width and height
        const pageWidth = 210; 
        const pageHeight = 297;

  // Set page dimensions and orientation
        doc.setPage(pageWidth, pageHeight);
        doc.setOrientation('landscape');

  // Render the stats HTML as PDF
        doc.html(statsEl, {
            callback: function (doc) {
            doc.save("github-stats.pdf");
            },
            x: 10,
            y: 10
        });
    });
};
