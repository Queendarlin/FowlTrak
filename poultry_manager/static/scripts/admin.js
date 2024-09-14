const sidebarToggle = document.querySelector("#sidebar-toggle");
sidebarToggle.addEventListener("click",function(){
    document.querySelector("#sidebar").classList.toggle("collapsed");
});

document.querySelector(".theme-toggle").addEventListener("click",() => {
    toggleLocalStorage();
    toggleRootClass();
});

function toggleRootClass(){
    const current = document.documentElement.getAttribute('data-bs-theme');
    const inverted = current == 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-bs-theme',inverted);
}

function toggleLocalStorage(){
    if(isLight()){
        localStorage.removeItem("light");
    }else{
        localStorage.setItem("light","set");
    }
}

function isLight(){
    return localStorage.getItem("light");
}

if(isLight()){
    toggleRootClass();
}


$(document).ready(function() {
    // Function to load modal content via AJAX
    $(document).on('click', '[data-bs-toggle="modal"]', function() {
        var url = $(this).attr('href');
        $.ajax({
            url: url,
            method: 'GET',
            success: function(data) {
                $('#editModal .modal-body').html(data);
            },
            error: function() {
                alert('Error loading the form.');
            }
        });
    });

    // Function to handle form submission via AJAX
    $(document).on('submit', '#editForm', function(e) {
        e.preventDefault(); // Prevent the default form submission
        var form = $(this);
        $.ajax({
            url: form.attr('action'),
            method: 'POST',
            data: form.serialize(),
            success: function(response) {
                $('#editModal').modal('hide'); // Hide the modal
                location.reload(); // Reload the page to reflect changes
            },
            error: function() {
                alert('Error saving the record.');
            }
        });
    });
});
