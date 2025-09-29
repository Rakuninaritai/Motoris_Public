function initializeLikeButton() {
    const likeButton = document.getElementById('like-button');
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (likeButton) {
        likeButton.addEventListener('click', function() {
            const productType = this.dataset.productType;
            const productId = this.dataset.productId;

            fetch(`/like/${productType}/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('like-count').textContent = data.like_count;
            })
            .catch(error => console.error('Error:', error));
        });
    }
}

document.addEventListener('DOMContentLoaded', initializeLikeButton);