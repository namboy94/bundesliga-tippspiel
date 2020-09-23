function moveSeasonPositionRow(teamId, shift) {

        if (shift !== -1 && shift !== 1) {
            return
        }

        let row = document.getElementById("position_row_" + teamId);
        let rowInput = row.getElementsByTagName("input")[0];
        let parent = row.parentNode;
        let rows = parent.getElementsByTagName("tr");
        let currentPosition = parseInt(rowInput.value);
        let rowIndex = currentPosition - 1;

        if (rowIndex + shift < 0 || rowIndex + shift >= rows.length) {
            return;
        }

        let neighbour = rows[rowIndex + shift];

        if (shift === -1) {
            parent.removeChild(row);
            parent.insertBefore(row, neighbour);
        } else {
            parent.removeChild(neighbour);
            parent.insertBefore(neighbour, row);
        }
        updateSeasonPosition(row, currentPosition + shift);
        updateSeasonPosition(neighbour, currentPosition);
    }
function updateSeasonPosition(row, position) {
    let rowInput = row.getElementsByTagName("input")[0];
    let rowPositionText = row.getElementsByTagName("span")[0];
    rowInput.value = position;
    rowPositionText.textContent = position;
}
