document.addEventListener('DOMContentLoaded', function() {
  const editModal = document.getElementById('editModal');
  const editForm = document.getElementById('editForm');
  const saveChangesButton = document.getElementById('saveChanges');

  // Load form into modal on Edit button click
  document.querySelectorAll('button[data-bs-target="#editModal"]').forEach(button => {
    button.addEventListener('click', function() {
      const model = this.getAttribute('data-model');
      const recordId = this.getAttribute('data-id');

      fetch(`/edit-record/${model}/${recordId}`)
        .then(response => response.text())
        .then(data => {
          editForm.innerHTML = data;  // Load the form into the modal body
        });
    });
  });

  // Handle form submission asynchronously
  saveChangesButton.addEventListener('click', function(event) {
    event.preventDefault();

    const formData = new FormData(editForm);
    const actionUrl = editForm.getAttribute('action');

    fetch(actionUrl, {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Close the modal and show success message
        alert('Record updated successfully!');
        editModal.modal('hide');
        location.reload();  // Optionally reload the page or update the UI
      } else {
        // Handle validation errors
        alert('Error updating record');
      }
    });
  });
});
