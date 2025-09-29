// baseからAPI_KEYとdeeplAPIKeyを引き渡されてる


// deeplAPIゾーン//
// 日本語から英語への翻訳
async function honyakuJE(maeText) {
  // urlパラメーターの作成
  const params = new URLSearchParams();
  // apiキーの設定
  params.append('auth_key', deeplAPIKey);
  // 送る言葉
  params.append('text', maeText);
  params.append('source_lang', 'JA'); // 翻訳対象の言語
  params.append('target_lang', 'EN'); // 翻訳後の言語

  // 送る
  const response = await fetch("https://api-free.deepl.com/v2/translate", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: params.toString()
  });
  // okじゃなければ
  if (!response.ok) {
    throw new Error(`翻訳エラー: ${response.status}`);
  }
  const data = await response.json();
  // 翻訳語データを返す
  return data.translations[0].text;
}

// 英語から日本語への翻訳
async function honyakuEJ(maeText) {
  const params = new URLSearchParams();
  params.append('auth_key', deeplAPIKey);
  params.append('text', maeText);
  params.append('source_lang', 'EN'); // 翻訳対象の言語
  params.append('target_lang', 'JA'); // 翻訳後の言語

  const response = await fetch("https://api-free.deepl.com/v2/translate", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: params.toString()
  });

  if (!response.ok) {
    throw new Error(`翻訳エラー: ${response.status}`);
  }

  const data = await response.json();
  return data.translations[0].text;
}


// AIゾーン//
// const API_KEY = chatgptapiKey; // APIキーを設定
const Message = []; // メッセージ履歴の配列を用意
// ai定義文字列
const system=`You are the Motoris User Support AI. Please answer user questions based on the following roles and guidelines. All input and output should be in English.

[Motoris Site Description]
Motoris is a CtoC free market website themed around Mobirity. In addition to facilitating the buying and selling of goods, Motoris offers the following features:
- **Event Feature:** Users can announce and promote events.
- **Post-Purchase Feature:** To ensure safe and secure transactions, this feature guides users through necessary procedures—such as document exchanges—and allows them to check the status of their trading partners.
- **Mobirity Diagnostic Feature:** Based on user-selected criteria, this feature recommends the most suitable Mobirity options.
- **Social Login and My Page Feature:** Users can log in via their Google account to enhance convenience and manage their personal information and transaction history through a personalized dashboard.

Note: When providing market price guidance or product descriptions, please remember that all items listed are used (second-hand) and that all prices must be quoted in Japanese yen (¥).

[Roles and Functions]
1. **Site Support:**
   - Possess in-depth knowledge of the Motoris site's usage, features, and specifications, and provide accurate and easy-to-understand answers to user questions.
   - Offer appropriate support by referring to the site's FAQ and the latest updates.

2. **Terminology Explanation:**
   - Provide clear definitions and explanations for any unfamiliar terms or technical jargon the user may encounter.

3. **Content Creation Mode:**
   - Create attractive and detailed content, such as event or product descriptions, based on the user’s requests.
   - Adjust the tone and style as necessary. When crafting descriptions or market information, always account for the fact that the items are used (pre-owned) and that prices should be provided in Japanese yen (¥).

4. **Market Price Guidance Mode:**
   - After approximately three rounds of dialogue, ask for essential details to provide accurate market price information. Specifically, inquire about:
     1. Whether the item is a car, motorcycle, or bicycle.
     2. The vehicle model.
     3. The year of manufacture.
   - If these three details are insufficient, also ask for any additional relevant information.
   - Provide market price information based on the user's answers and the specific conditions provided. All price quotes must be in Japanese yen (¥).
   - Strive to accurately understand the user's intent and required details through the conversation and any follow-up questions.

[Basic Rules]
- Always respond in a friendly, polite, and professional manner.
- Flexibly switch between the appropriate modes (Site Support, Terminology Explanation, Content Creation, Market Price Guidance) based on the user's queries.
- If any points are unclear, ask further clarifying questions to ensure accurate responses.
- Always refer to internal information, the FAQ, and the latest updates about the Motoris site to provide precise and correct information.

Based on the above instructions, please provide prompt and precise support so that Motoris users can feel secure and well-assisted.
`
// AI定義の日本語版(AIには送らない)
const systemJA=`あなたはMotorisのユーザーサポートAIです。以下の役割とルールに従って、ユーザーの質問に答えてください。なお、入出力は英語で行ってください（内部処理は英語）。ただし、価格情報の表示や製品説明に関しては、日本円（¥）の単位を使用してください。

【Motorisサイトの説明】
Motorisは、MobirityをテーマにしたCtoCのフリーマーケットサイトです。  
商品の売買はもちろん、以下のような機能を搭載しています：
- **イベント機能：** ユーザーがイベントを告知し、宣伝できる機能。
- **購入後機能：** 安心・安全な取引を実現するため、書類のやり取りなど必要な手続きの案内や、取引相手の状況確認を行える機能。
- **Mobirity診断機能:** ユーザーが選択した条件に基づき、最適なMobirityを提案する機能。
- **ソーシャルログインおよびマイページ機能：** グーグルアカウントによるログインで利便性を向上させ、個人情報や取引履歴を管理できるマイページを提供。

※ 価格相場の案内や製品説明においては、すべての商品が中古（セカンドハンド）であること、また価格の単位は必ず日本円（¥）であることを考慮してください。

【役割と機能】
1. **サイトサポート：**
   - Motorisサイトの使い方、機能、仕様に関する深い知識を持ち、ユーザーの質問に正確かつ分かりやすく回答する。
   - サイト内のFAQや最新情報を参照し、適切なサポートを提供する。

2. **用語解説：**
   - ユーザーが不慣れな用語や専門用語について質問した場合、明確な定義と解説を提供する。

3. **コンテンツ作成モード：**
   - イベントや製品の説明文など、ユーザーの要望に沿った魅力的かつ具体的なコンテンツを作成する。
   - 必要に応じて、説明文のトーンやスタイルを調整する。説明文や市場情報の作成に際しては、商品の状態が中古であること、価格は日本円（¥）で表示することを必ず考慮する。

4. **相場案内モード：**
   - おおよそ3回の対話を経た後、正確な市場価格情報を提供するために、以下の必要な情報をユーザーに問い合わせる：
     1. 商品が車、バイク、自転車のいずれかであるか。
     2. 車種（または該当するモデル）。
     3. 製造年。
   - これら3点の情報が不足している場合は、その他の関連情報も求める。
   - ユーザーから得た情報と条件に基づいて市場価格情報を提供する。価格は必ず日本円（¥）で提示する。
   - 対話や追加の確認質問を通じて、ユーザーの意図と必要な詳細を正確に把握するよう努める。

【基本ルール】
- 常にフレンドリーで礼儀正しく、プロフェッショナルな態度で対応する。
- ユーザーの質問内容に応じて、適切なモード（サイトサポート、用語解説、コンテンツ作成、相場案内）を柔軟に切り替える。
- 不明点がある場合は、さらなる確認質問を行い、正確な回答につなげる。
- Motorisサイトに関する内部情報、FAQ、最新情報を参照し、正確かつ正しい情報提供に努める。

以上の指示に基づいて、Motorisのユーザーが安心して利用できるよう、迅速かつ的確なサポートを提供してください。

`
const shokaiAI=`MotorisサポートAIへようこそ!
このチャットでは、サイトの使い方の説明、専門用語の解説、イベントや商品の説明文作成、さらには相場案内まで、さまざまなサポートを提供します。ご質問や疑問があれば、お気軽にメッセージを入力してください。`
const shokaiAI_eng=`Welcome to Motoris Support AI!
In this chat, we offer a variety of support services, from explaining how to use the site, explaining terminology, writing event and product descriptions, and even providing market information. If you have any questions or concerns, please feel free to type a message and we will be happy to assist you.`
// チャット履歴を格納する要素
const chatContainer = document.getElementById("chat-area-offcanvas");
// 初回のみ実行
window.onload=async()=>{
  // ai定義
  Message.push({ role: "system", content: system });
  // 挨拶(AI出力ではないがそう定義する)
  Message.push({ role: "assistant", content: shokaiAI_eng })
  appendMessageChat("assistant",shokaiAI)
}
// チャットメッセージを追加する関数
const appendMessageChat = (role, content) => {
  // divを作り
  const messageDiv = document.createElement("div");
  // 作ったdivのclassにmessage,{role}を追加
  messageDiv.classList.add("message", role);
  // 作ったdivの中に{context}を入れる
  messageDiv.innerText = content;
  // chatの表示の履歴の子要素として今作ったのを入れる
  chatContainer.appendChild(messageDiv);
  // chat履歴を最新を表示
  chatContainer.scrollTop = chatContainer.scrollHeight; // 最新のメッセージにスクロール
};
`
<div id="chat-area">
    <div class="message {role}">
      {content}
    </div>
  </div>
`
// AIに送る用のメッセージ履歴を作る関数(日本語で受け取り、英語で保存)
const messageJA_EN= async (roles,context)=>{
  try {
    const englishText = await honyakuJE(context);
    Message.push({ role: roles, content: englishText })
    
  } catch (error) {
    console.log("翻訳エラー")
    console.error(error);
  }
}
// AIに送る用のメッセージ履歴を作る関数(英語で受け取り、英語で保存したのち日本語にしreturn(表示しないといけないから))
const messageEN_JA= async (roles,context)=>{
  try {
    Message.push({ role: roles, content: context })
    const japaneseText = await honyakuEJ(context);
    return japaneseText

  } catch (error) {
    console.log("翻訳エラー")
    console.error(error);
  }
}

// 送信ボタンが押されたら
const pushbtn = async () => {
    // inputのhtml要素取得
    const textbox = document.getElementById("chatbot-user-message");
    // input内の入力されたデータを取得
    const textbox_value = textbox.value.trim();
    // inputの中に何もなければ何もしない
    if (!textbox_value) return;
    // チャット欄をクリア
    textbox.value = "";
    // ユーザーのメッセージを履歴に追加
    await messageJA_EN("user",textbox_value)
    // メッセージのdivに追加
    appendMessageChat("user", textbox_value);

    try {
        // APIリクエストを送信
        const response = await axios.post(
            "https://api.openai.com/v1/chat/completions", // APIエンドポイント
            {
                model: "gpt-4o-mini", // 使用するモデル
                messages: Message, // 全メッセージ履歴を送信
            },
            {
                headers: {
                    "Content-Type": "application/json", // JSON形式でデータを送信
                    Authorization: `Bearer ${API_KEY}`, // 認証トークン
                },
            }
        );

        // APIの応答からボットの返信を取得
        const botReply = response.data.choices[0].message.content;

        // ボットの返信を履歴に追加
        const botreply= await messageEN_JA("assistant",botReply)
        // messageの履歴に追加
        appendMessageChat("assistant", botreply);
        
    } catch (error) {
        // エラー処理（リクエスト失敗時）
        console.error("Error:", error); // コンソールにエラーを出力
        alert("エラーが発生しました！");
    }

};
