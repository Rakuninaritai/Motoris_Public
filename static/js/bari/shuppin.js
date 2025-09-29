// 既存の表示されている画像プレビュー（.image-preview-item）のうち、削除チェックボックスが付いている場合は、そのチェック状態を確認して有効な画像としてカウントする
function validateImageCount() {
  let validCount = 0;

  // 表示されている既存画像のプレビュー要素を取得
  const existingItems = document.querySelectorAll(".image-preview-item");
  console.log("既存の表示画像数:", existingItems.length);
  
  existingItems.forEach(function(item) {
    // 各 .image-preview-item 内にある削除チェックボックスを探す
    const checkbox = item.querySelector("input[type='checkbox'][name$='-DELETE']");
    if (checkbox) {
      // チェックがついていなければ、その画像は有効とみなす
      if (!checkbox.checked) {
        validCount++;
      }
    } else {
      // チェックボックスが無い場合は（通常は既存画像がある場合必ずチェックボックスがあるはずですが）、
      // とりあえずその画像を有効とみなす
      validCount++;
    }
  });

  // 追加画像用の input のファイル数をカウント
  const additionalInput = document.getElementById("additional-files");
  let additionalCount = 0;
  if (additionalInput && additionalInput.files) {
    additionalCount = additionalInput.files.length;
    validCount += additionalCount;
  }
  console.log("追加画像の数:", additionalCount);
  console.log("合計有効画像数:", validCount);

  return validCount;
}

// document.addEventListener("DOMContentLoaded", function () {
//   const carForm = document.getElementById("car-form");
//   if (!carForm) {
//     console.error("car-form が見つかりません");
//     return;
//   }
  
//   // フォームが「編集モード」(data-edit 属性が "true") の場合のみ、submit イベントにバインドする
//   if (carForm.getAttribute("data-edit") === "true") {
//     carForm.addEventListener("submit", function(e) {
//       const count = validateImageCount();
//       console.log("submit 時の画像カウント:", count);
//       // もし有効な画像の合計が 1 枚未満なら、フォーム送信を中止してアラート表示
//       if (count < 1) {
//         e.preventDefault();
//         alert("少なくとも1枚の画像が必要です。");
//       }
//     });
//   }
// });
// html二も書いてある出品時に実行するやつonclick(編集時は数数えだから)
function multipleFunction() {
  for (let i = 0; i < document.getElementById('multiple-files').files.length; i++) {
      const dt = new DataTransfer();
      dt.items.add(document.getElementById('multiple-files').files[i]);
      document.getElementById("id_form-%number-files".replace("%number", i)).files = dt.files;
  }
}
// 編集時に数を数える関数
function validateAndSubmit() {
  // validateImageCount() は画像枚数を返す関数です
  const count = validateImageCount();
  console.log("画像の数:", count);
  if (count < 1) {
    alert("少なくとも1枚の画像が必要です。");
    // 送信をキャンセルするために false を返す
    return false;
  }
  // もし追加で multipleFunction() を実行する必要があるならここで呼び出す
  multipleFunction();
  // 条件を満たすのでフォーム送信を継続
  return true;
}

