const logoutLink = document.getElementById('logout-link');

    logoutLink.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent default navigation

        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, log me out!',
            cancelButtonText: 'Cancel'
        }).then((result) => {
            if (result.isConfirmed) {
                // Redirect to logout URL if confirmed
                window.location.href = logoutLink.href;
            }
        });
    });