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
