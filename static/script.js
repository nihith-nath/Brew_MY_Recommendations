$(document).ready(function () {
    console.log("Document ready!");  // Check if document is ready

    $('.toggle-button').click(function () {
        console.log("Button clicked:", this.name);  // Check if button click is detected
        $(this).toggleClass('active');

        let hiddenInput = $('input[name="' + this.name + '"]');
        if ($(this).hasClass('active')) {
            hiddenInput.val('1');
        } else {
            hiddenInput.val('');
        }

        let anyActive = $('.toggle-button.active').length > 0;
        if (anyActive) {
            $('#recommendationsOutput').show();
        } else {
            $('#recommendationsOutput').hide();
        }
    });
});

document.getElementById('recommendationForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var formData = new FormData(this);

    fetch('/recommend', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        var recommendationsDiv = document.getElementById('recommendationsOutput');
        recommendationsDiv.innerHTML = '<h2>Based on your Favourite drinks ☕ we think you will love 💚 these drinks.. </h2>'; // Clear previous recommendations
       
        if (data.recommendations && data.recommendations.length > 0) {
            var ul = document.createElement('ol');
            data.recommendations.forEach(function(drink) {
                var li = document.createElement('li');
                li.textContent = `${drink.Drink_name}`;
                ul.appendChild(li);
            });
            recommendationsDiv.appendChild(ul);
        } else {
            recommendationsDiv.textContent = ' No drinks Selected';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('recommendationsOutput').textContent = 'An error occurred while fetching recommendations.';
    });
});