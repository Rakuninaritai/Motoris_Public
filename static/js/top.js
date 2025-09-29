// Splideの初期化
new Splide("#splide1", {
  autoplay: false,            // 自動再生
  type:"slide",              // slide(ループさせずにある分だけ)
  perPage: 4,                // 3枚表示
   // レスポンシブ切り替え用の設定
   breakpoints: {
    // 991px 以下になったら perPage=2
    991: {
      perPage: 2,
    },
    // 767px 以下になったら perPage=1
    767: {
      perPage: 1,
    },
  },
  focus: 0,                  // ページネーション数がスライド数になる
  pauseOnHover: false,       // カーソルが乗ってもスクロールを停止させない
  pauseOnFocus: false,       // 自動再生の間隔
  speed: 600,                // スライダーの移動時間
  pagination: false,//  中黒で今のスライド位置表示するやつ消す
}).mount();

new Splide("#splide2", {
  autoplay: false,            // 自動再生
  type:"slide",              // slide(ループさせずにある分だけ)
  perPage: 4,                // 3枚表示
  // レスポンシブ切り替え用の設定
  breakpoints: {
    // 991px 以下になったら perPage=2
    991: {
      perPage: 2,
    },
    // 767px 以下になったら perPage=1
    767: {
      perPage: 1,
    },
  },
  focus: 0,                  // ページネーション数がスライド数になる
  pauseOnHover: false,       // カーソルが乗ってもスクロールを停止させない
  pauseOnFocus: false,       // 自動再生の間隔
  speed: 600,                // スライダーの移動時間
  pagination: false,//  中黒で今のスライド位置表示するやつ消す
}).mount();

new Splide("#splide3", {
  autoplay: false,            // 自動再生
  type:"slide",              // slide(ループさせずにある分だけ)
  perPage: 4,                // 3枚表示
  // レスポンシブ切り替え用の設定
  breakpoints: {
    // 991px 以下になったら perPage=2
    991: {
      perPage: 2,
    },
    // 767px 以下になったら perPage=1
    767: {
      perPage: 1,
    },
  },
  focus: 0,                  // ページネーション数がスライド数になる
  pauseOnHover: false,       // カーソルが乗ってもスクロールを停止させない
  pauseOnFocus: false,       // 自動再生の間隔
  speed: 600,                // スライダーの移動時間
  pagination: false,//  中黒で今のスライド位置表示するやつ消す
}).mount();

new Splide("#splide4", {
  autoplay: false,            // 自動再生
  type:"slide",              // slide(ループさせずにある分だけ)
  perPage: 4,                // 3枚表示
  // レスポンシブ切り替え用の設定
  breakpoints: {
    // 991px 以下になったら perPage=2
    991: {
      perPage: 2,
    },
    // 767px 以下になったら perPage=1
    767: {
      perPage: 1,
    },
  },
  focus: 0,                  // ページネーション数がスライド数になる
  pauseOnHover: false,       // カーソルが乗ってもスクロールを停止させない
  pauseOnFocus: false,       // 自動再生の間隔
  speed: 600,                // スライダーの移動時間
  pagination: false,//  中黒で今のスライド位置表示するやつ消す
}).mount();

