$(function() {
                $('#btnSignUp').click(function() {

                $.ajax({
                    url: '/signUp',
                    data: $('form').serialize(),
                    type: 'POST',
                    success: function(response) {
                        window.location.href = "/profile";
                        console.log(response);
                    },
                error: function(error) {
                    console.log(error);
                        }
                    });
                });
            });