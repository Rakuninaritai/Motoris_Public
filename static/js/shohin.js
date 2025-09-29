// 写真スライド機能
let currentSlideIndex = 0;
let slides;

document.addEventListener('DOMContentLoaded', function() {
    slides = document.querySelectorAll('.slide');
    
    // 最初のスライドを表示
    if (slides.length > 0) {
        slides[0].style.display = "block";
    }
});

// グローバルスコープでmoveSlide関数を定義
window.moveSlide = function(direction) {
    if (!slides || slides.length === 0) return;
    
    slides[currentSlideIndex].style.display = "none";
    currentSlideIndex = (currentSlideIndex + direction + slides.length) % slides.length;
    slides[currentSlideIndex].style.display = "block";
}

// いいね機能
// いいね機能
document.addEventListener('DOMContentLoaded', function() {
    const likeButton = document.getElementById('like-button');
    const likeCountDisplay = document.getElementById('like-count');

    if (likeButton && likeCountDisplay) {
        const productType = likeButton.getAttribute('data-product-type');
        const productId = likeButton.getAttribute('data-product-id');

        // CSRFトークンを取得する関数
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        // 初期状態でいいね数を取得
        fetch(`/shohin/like-status/${productType}/${productId}/`)
            .then(response => response.json())
            .then(data => {
                likeCountDisplay.textContent = data.like_count;
                if (data.liked) {
                    likeButton.classList.add('active');
                }
            });

        // いいねボタンのクリックイベント
        likeButton.addEventListener('click', function() {
            fetch(`/shohin/like/${productType}/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    likeButton.classList.add('active');
                } else {
                    likeButton.classList.remove('active');
                }
                likeCountDisplay.textContent = data.like_count;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});

// コメント管理のための拡張スクリプト
document.addEventListener('DOMContentLoaded', function() {
    const commentForm = document.querySelector('.comment-input-section form');
    const commentList = document.getElementById('comment-list');

    if (commentForm) {
        commentForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const formData = new FormData(this);
            const submitButton = this.querySelector('button[type="submit"]');
            
            // ボタンを一時的に無効化
            submitButton.disabled = true;
            
            // CSRFトークンの取得
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrftoken
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(() => {
                // フォームをリセット
                commentForm.reset();
                
                // ページをリロード（新しいコメントを表示するため）
                window.location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('コメントの送信中にエラーが発生しました。');
            })
            .finally(() => {
                // ボタンを再度有効化
                submitButton.disabled = false;
            });
        });
    }

    // コメントリストが存在する場合、最下部にスクロール
    if (commentList) {
        commentList.scrollTop = commentList.scrollHeight;
    }
});

// LocalStorage関連の機能を削除（Djangoのバックエンドに完全に移行）