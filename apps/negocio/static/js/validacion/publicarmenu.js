$(function() {

    $("#menuForm").validate({
    
        rules: {
            nombre: {
                required: true,
                maxlength: 45
            },
            breve_descripcion: {
                required: true,
                maxlength: 80
            },
            descripcion: {
                required: true
            },
            precio: {
                required: true,
                number: true
            },
            tipo_entrega: {
                required: true
            },
            direccion: {
                required: true
            },
            cantidad_maxima: {
                required: true
            }
        },
        
        messages: {
            nombre: {
                required: "Ingrese nombre",
                maxlength: "Demasiados caracteres"
            },
            breve_descripcion: {
                required: "Ingrese descripcion",
                maxlength: "Demasiados caracteres"
            },
            descripcion: {
                required: "Ingrese descripcion"
            },
            precio: {
                required: "Ingrese precio",
                number: "Solo numeros"
            },
            tipo_entrega: {
                required: "Seleccione Tipo Entrega"
            },
            direccion: {
                required: "Ingrese direccion"
            },
            cantidad_maxima: {
                required: "Seleccione la cantidad maxima que puede ofrecer"
            }
        },

    });

});