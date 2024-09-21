$(document).ready(function () {
  // Function to load modal content via AJAX
  $(document).on('click', '[data-bs-toggle="modal"]', function () {
    var url = $(this).attr('href');
    $.ajax({
      url: url,
      method: 'GET',
      success: function (data) {
        $('#editModal .modal-body').html(data);
      },
      error: function () {
        alert('Error loading the form.');
      },
    });
  });

  // Function to handle form submission via AJAX
  $(document).on('submit', '#editForm', function (e) {
    e.preventDefault();
    var form = $(this);
    $.ajax({
      url: form.attr('action'),
      method: 'POST',
      data: form.serialize(),
      success: function (response) {
        $('#editModal').modal('hide');
        location.reload();
      },
      error: function () {
        alert('Error saving the record.');
      },
    });
  });
});
