// バリデーション用js(accounts)

//ユーザーネームメルアドフィールドを取得(ログインページページ)(ばりでなしにつきテンプレとして使用中)
const usernameemail = document.getElementById('usernameemail');
// ユーザーネームメルアドフィールドがあれば
if (usernameemail) {
    // ユーザーネームメルアドフィールドのhtml属性にpattarnを追加しその値は''です。
    // usernameemail.setAttribute('pattern', '^[^\\x01-\\x7E\\xA1-\\xDF]+$');
    // usernameemail.setAttribute('title', '全角文字のみを入力してください');
}

// パスワードのフィールド(ログインページ、登録ページ(上だけ))//再度のパスワードはサーバー側で判別するだけだからバリでいらんかな
// パスワードは送信の時点でハッシュ化(セキュリティのため元の文字列を分からなくする処理)されてしまいpattarnでの検証ができないので入力されたら検証としている。
const id_password = document.getElementById('id_password');
//パスワードのエラー表示部分(デフォルト非表示)
const pwer = document.getElementById('pwer');
// ボタンを取得(pwのエラーは手動なのでbtnを無効化して先に進めないようにしないといけない。)
// htmlpattarnやほかのやつはhtmlの機能使えているのでサーバーに送れないがこれはエラーメッセージ出しているだけなので
const btn = document.getElementById("btn");
//正規表現
const pattern = /(?=.*[a-zA-Z])(?=.*\d|.*\W).{8,}/;
//エラー表示初期化デフォルト消す
pwer.classList.add("d-none");
//ボタンデフォルトは使える(無効にする処理をfalseに)
btn.disabled = false;
//パスワードが入力されたら…
id_password.addEventListener('input', () => {
    // 入力された値を取得
    const value = id_password.value;
    //trueなら(バリデーション通ったら)
    if (pattern.test(value)) {
        // d-noneを付けて非表示、ボタン有効
        pwer.classList.add("d-none");
        btn.disabled = false;

    } else {
        //通らなかったら表示
        pwer.classList.remove("d-none");
        btn.disabled = true;
    };
});

//ユーザーネームのフィールド(登録ページ)
const username = document.getElementById('username');
if (username) {
    // username.setAttribute('pattern', '^[^\\x01-\\x7E\\xA1-\\xDF]+$');
    // username.setAttribute('title', '全角文字のみを入力してください');
}

//メルアドのフィールド(登録ページ)
const eail = document.getElementById('email');
if (email) {
    // email.setAttribute('pattern', '^[^\\x01-\\x7E\\xA1-\\xDF]+$');
    // email.setAttribute('title', '全角文字のみを入力してください');
}



