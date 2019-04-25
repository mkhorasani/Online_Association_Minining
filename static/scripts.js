$(document).ready(function() {
    // Trigger click from pretty choose file button
    $("#trans_file_nice_button").click(function(event) {
        event.preventDefault();
        $("#transactions_file").click();
    });

    // Display chosen file name
    $("#transactions_file").on("change", function() {
        var filename = $("#transactions_file").val().split('\\').pop();
        $("#selected_file_name").text(filename);
    });
});
