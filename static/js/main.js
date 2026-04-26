// ── RECHERCHE PATIENT TABLEAU DE BORD ──
function rechercherPatient() {
    const input = document.getElementById('searchInput');
    if (!input) return;
    const valeur = input.value.toLowerCase();
    const rows = document.querySelectorAll('#patientBody tr');
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(valeur) ? '' : 'none';
    });
}