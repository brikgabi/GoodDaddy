$(function() {
                $('#btnSignIn').click(function() {

                $.ajax({
                    url: '/signIn',
                    data: $('form').serialize(),
                    type: 'POST',
                    success: function(response) {
                        window.location.href = "/profile";
                        console.log(error);
                    },
                error: function(error) {
                    console.log(error);
                        }
                    });
                });
            });