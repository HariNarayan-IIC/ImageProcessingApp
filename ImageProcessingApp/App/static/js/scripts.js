$(document).ready(function(){
    $('#Category').change(function() {
        var categoryId = $(this).val();
        $.ajax({
            url: '{% url "ajax_load_operations" %}',
            data: {
                'category_id': categoryId
            },
            success: function(data) {
                $('#Operation').html('<option value="">Select Operation</option>');
                data.forEach(function(operation) {
                    $('#Operation').append('<option value="' + operation.id + '">' + operation.name + '</option>');
                });
            }
        });
    });

    $('#Operation').change(function() {
        var operationId = $(this).val();
        $.ajax({
            url: '{% url "ajax_load_parameters" %}',
            data: {
                'operation_id': operationId
            },
            success: function(data) {
                $('#parameters').empty();
                data.forEach(function(parameter) {
                    $('#parameters').append('<label for="' + parameter.id + '">' + parameter.name + ' (' + parameter.valueType + '):</label>');
                    $('#parameters').append('<input type="' + parameter.valueType + 'class = "form-control"' + '" id="' + parameter.id + '" name="' + parameter.name + '"><br>');
                });
            }
        });
    });

    // Handle click event on pencil icon
    // {% comment %} $('#update').click(function() {
    //     console.log("I am here");
    //     $('#updateModal').modal('show');
    // }); 

    // const myModal = document.getElementById('myModal')
    // const myInput = document.getElementById('myInput')

    // myModal.addEventListener('shown.bs.modal', () => {
    // myInput.focus()
    // }){% endcomment %}

});