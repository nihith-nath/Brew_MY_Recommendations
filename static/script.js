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
    e.preventDefault(); // Prevent default form submission
    
    var formData = new FormData(this);

    fetch('/recommend', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        var recommendationsDiv = document.getElementById('recommendationsOutput');
        recommendationsDiv.innerHTML = ''; // Clear previous recommendations
        
        if (data.recommendations && data.recommendations.length > 0) {
            var h2 = document.createElement('h2');
            h2.textContent = 'Based on your Favorite drinks ☕ we think you will love 💚 these drinks..';
            recommendationsDiv.appendChild(h2);
            
            var ul = document.createElement('ol');
            data.recommendations.forEach(function(drink) {
                var li = document.createElement('li');
                li.textContent = drink.Drink_name;
                ul.appendChild(li);
            });
            recommendationsDiv.appendChild(ul);

            // Add collaboration invitation
            var collaborationText = document.createElement('div');
            collaborationText.className = 'collaboration-text';
            collaborationText.innerHTML = `<h3>Intrigued by the Fusion of Coffee and Data?</h3>
                                            <p>If you're excited about this blend of coffee and data science, or if you have ideas for collaboration, let's connect!<br><br>
                                            Reach out to me at <a href="mailto:nihithna@buffalo.edu">nihithna@buffalo.edu</a>. Together, we can brew something innovative!</p>`;
            recommendationsDiv.appendChild(collaborationText);
            
            // Add Clear Drinks button
            var clearButton = document.createElement('button');
            clearButton.type = 'button';
            clearButton.className = 'btn btn-outline-danger';
            clearButton.textContent = 'Clear Drinks';
            clearButton.addEventListener('click', function() {
                location.reload(); // Reload the page
            });
            recommendationsDiv.appendChild(clearButton);
        } else {
            var noResult = document.createElement('p');
            noResult.textContent = 'No drinks selected';
            recommendationsDiv.appendChild(noResult);
        }

        // Scroll to recommendationsOutput div
        recommendationsDiv.scrollIntoView({ behavior: 'smooth' });
    })
    .catch(error => {
        console.error('Error:', error);

        var errorDiv = document.getElementById('recommendationsOutput');
        errorDiv.textContent = 'An error occurred while fetching recommendations.';
    });
});

function searchDrinks() {
    const input = document.getElementById('searchInput').value.toLowerCase();
    const labels = document.querySelectorAll('.sections label');

    labels.forEach(label => {
        const text = label.textContent.toLowerCase();
        if (text.includes(input)) {
            label.style.display = '';
        } else {
            label.style.display = 'none';
        }
    });

    return false; // Prevent form submission
}
