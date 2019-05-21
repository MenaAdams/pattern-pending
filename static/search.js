
function showYarn() {
    $('#search-form').toggle();
    $('#yarn-dropdown').toggle();
}

function showPatt() {
    $('#search-form').toggle();
    $('#pattern_dropdown').toggle();
}

function showBoth() {
    $('#search-form').toggle();
    $('#pattern_dropdown').toggle();
    $('#yarn-dropdown').toggle();
}

$('#yarn-search').on('click', showYarn);
$('#patt-type-button').on('click', showPatt);
$('#search_w_both').on('click', showBoth);
