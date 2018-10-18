//triggered when modal is about to be shown
$('#deleteModal').on('show.bs.modal', function(e) {
    var action = e.relatedTarget.dataset.action;
    $('#deleteForm').attr("action", action);
});
