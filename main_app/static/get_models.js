// get_models.js

document.addEventListener('DOMContentLoaded', function() {
    var makeDropdown = document.getElementById('make');
    var modelDropdown = document.getElementById('model');

    makeDropdown.onchange = function() {
        modelDropdown.innerHTML = '<option value="">Select Model</option>';

        if (makeId) {
            // Update this URL to the correct endpoint in your Django app
            var url = "{% url 'get-models' %}";
            fetch(url + '?make_id=' + makeId)
            // fetch(`/ajax/get-models/?make_id=${makeId}`)
                .then(response => response.json())
                .then(data => {
                    data.models.forEach(function(model) {
                        var opt = document.createElement('option');
                        opt.value = model[0];  // Assuming model is a tuple where model[0] is the id
                        opt.innerHTML = model[1];  // Assuming model[1] is the name
                        modelDropdown.appendChild(opt);
                    });
                })
                .catch(error => console.error('Error:', error));
        }
    };
});
