$(function() {

    $("#registroUsuarioForm").validate({
    
        rules: {
            first_name: {
                required: true
            },
            last_name: {
                required: true
            },
            celular: {
                required: true
            },
            email: {
                required: true,
                email: true
            },
            password: {
                required: true,
                minlength: 6
            },
            password_confirmation : {
                minlength : 6,
                equalTo : "#password"
            }
        },
        
        messages: {
            first_name: {
                required: "Ingrese nombres"
            },
            last_name: {
                required: "Ingrese apellidos"
            },
            celular: {
                required: "Ingrese celular"
            },
            email: {
                required: "Ingrese email",
                email: "Ingrese un email valido"
            },
            password: {
                required: "Ingrese contraseña",
                minlength: "Contraseña minimo 6 caracteres"
            },
            password_confirmation: {
                required: "Ingrese contraseña de confirmacion",
                minlength: "Contraseña minimo 6 caracteres",
                equalTo : "Contraseña no coincide"
            }
        },

    });

});