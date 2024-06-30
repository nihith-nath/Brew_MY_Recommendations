$(document).ready(function() {
    let selectedDrinks = [];
    let filters = {};

    function getRecommendations() {
        const n_recommendations = $('#n_recommendations').val();
        $.ajax({
            type: 'POST',
            url: '/recommend',
            data: {
                selected_drinks: selectedDrinks,
                include_all: filters.include_all ? '1' : '0',
                include_coffee: filters.include_coffee ? '1' : '0',
                include_tea: filters.include_tea ? '1' : '0',
                include_neither: filters.include_neither ? '1' : '0',
                include_hot: filters.include_hot ? '1' : '0',
                include_cold: filters.include_cold ? '1' : '0',
                include_frozen: filters.include_frozen ? '1' : '0',
                n_recommendations: n_recommendations
            },
            success: function(response) {
                $('#recommendationList').html(response);
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    }

    $('.drink-button').on('click', function() {
        const drink = $(this).data('drink');
        const index = selectedDrinks.indexOf(drink);
        if (index > -1) {
            selectedDrinks.splice(index, 1);
            $(this).removeClass('selected');
        } else {
            selectedDrinks.push(drink);
            $(this).addClass('selected');
        }
        getRecommendations();
    });

    $('.filter-button').on('click', function() {
        const filter = $(this).data('filter');
        filters[filter] = !filters[filter];
        $(this).toggleClass('selected');
        getRecommendations();
    });

    $('#n_recommendations').on('change', function() {
        getRecommendations();
    });

    // Initial load
    getRecommendations();
});

$(document).ready(function() {
    $('#recommendations').on('click', function(event) {
        event.preventDefault();

        // Gather selected drink preferences
        var selectedDrinks = [];
        $('input[name="drinks"]:checked').each(function() {
            selectedDrinks.push($(this).val());
        });

        // Log the selected drinks to the console
        console.log('Selected Drinks:', selectedDrinks);

        // Make AJAX request
        $.ajax({
            type: 'POST',
            url: '/recommend',
            contentType: 'application/json',
            data: JSON.stringify({ drinks: selectedDrinks }),
            success: function(response) {
                // Update recommendations div with received data
                var recommendationsHtml = '<h3>Your Top Recommendations:</h3><ul>';
                response.recommendations.forEach(function(item) {
                    recommendationsHtml += '<li>' + item.Drink_name + ' (Distance: ' + item.distance.toFixed(2) + ')</li>';
                });
                recommendationsHtml += '</ul>';
                $('#recommendations').html(recommendationsHtml);
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    });
});
