$(document).ready(function(){
    $('#category').change(function() {
        var categoryId = $(this).val();
        $.ajax({
            url: '{% url "ajax_load_operations" %}',
            data: {
                'category_id': categoryId
            },
            success: function(data) {
                $('#operation').html('<option value="">Select Operation</option>');
                data.forEach(function(operation) {
                    $('#operation').append('<option value="' + operation.id + '">' + operation.name + '</option>');
                });
            }
        });
    });

    $('#operation').change(function() {
        var operationId = $(this).val();
        $.ajax({
            url: '{% url "ajax_load_parameters" %}',
            data: {
                'operation_id': operationId
            },
            success: function(data) {
                $('#parameters').empty();
                data.forEach(function(parameter) {
                    $('#parameters').append('<label for="' + parameter.id + '">' + parameter.name + ' (' + parameter.value_type + '):</label>');
                    $('#parameters').append('<input type="' + parameter.value_type + '" id="' + parameter.id + '" name="' + parameter.name + '"><br>');
                });
            }
        });
    });
})