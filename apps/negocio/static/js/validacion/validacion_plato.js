$(function() {

    $("#platoForm").validate({
    
        rules: {
            nombre: {
                required: true,
                maxlength: 45
            },
            ingredientes: {
                required: true
            },
            tipo_plato: {
                required: true
            }
        },
        
        messages: {
            nombre: {
                required: "Ingrese nombre",
                maxlength: "Demasiados caracteres"
            },
            ingredientes: {
                required: "La lista de ingredientes"
            },
            tipo_plato: {
                required: "Seleccione Tipo Plato"
            }
        },

    });

});