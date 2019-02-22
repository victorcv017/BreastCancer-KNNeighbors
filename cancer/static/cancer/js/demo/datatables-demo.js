// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable({
    "dom": 'rtp',
    "lengthChange": false,
    "iDisplayLength": 3,
    "language": {
      "paginate": {
        "previous": "Anterior",
        "next" : "Siguiente"
      }
    }
  }
  );
});
