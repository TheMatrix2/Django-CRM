$(document).ready(function() {
      $('table tbody tr').click(function() {
        var clientId = $(this).data('id');
        window.location.href = '/client/' + clientId;
      });
    });