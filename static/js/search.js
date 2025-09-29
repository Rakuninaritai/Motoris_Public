window.onload=function(){
  //最初にどのmobirityを表示しなければいけないか取得(trimで空白を除外)
  const mbb=document.getElementById("mbb").textContent.trim();
  //その値を
  const mbs=document.getElementById("mbs");
  //選択させる
  mbs.value=mbb;



  //選択された値に応じて表示内容を変更
  sentahyouzi();
}

// 選択されたのを表示(formとdb)
function sentahyouzi(){
  // 何が選択されているか
  const mbs=document.getElementById("mbs");
  // 取得してsentakuに
  const sentaku=mbs.value;

  // どのmobirityが検索されたか
  const mbb=document.getElementById("mbb").textContent.trim();

  // db位置
  // 総合dbの表示位置
  const sougoudbhyouzi=document.getElementById("sougoudbhyouzi");
  // カーdbの表示位置
  const cardbhyouzi = document.getElementById("cardbhyouzi");
  // 自転車dbの表示位置
  const bydbhyouzi = document.getElementById("bydbhyouzi");
  // バイクdbの表示位置
  const mcdbhyouzi = document.getElementById("mcdbhyouzi");

  //form位置(以下formはfmとする) 
  // 総合fm表示位置
  const sougoufmhyouzi=document.getElementById("sougoufmhyouzi");
  // 検索文字表示位置
  const kensakumz=document.getElementById("kensakumz");
  // 車fm表示位置
  const carfmhyouzi=document.getElementById("carfmhyouzi");
  // バイクfm表示位置
  const mcfmhyouzi=document.getElementById("mcfmhyouzi");
  // 自転車fm表示位置
  const byfmhyouzi=document.getElementById("byfmhyouzi");

  // タイトル表示位置
  const sougoumz=document.getElementById("sougoumz");
  const carmz=document.getElementById("carmz");
  const mcmz=document.getElementById("mcmz");
  const bymz=document.getElementById("bymz");

  // 絞り込み文字表示位置
  const kenkomz=document.getElementById("kenkomz");

  // 全部にd-none付与で初期化(一度非表示に、前に実行して表示されている可能性があるから)
  // displaynoneなどではない理由はカード横並びのブーストとdisplayは合わないため。
  // .classlist.addはついていなければ付加する。あればなにもしない
  // db
  sougoudbhyouzi.classList.add("d-none");
  cardbhyouzi.classList.add("d-none");
  bydbhyouzi.classList.add("d-none");
  mcdbhyouzi.classList.add("d-none");

  //fm
  sougoufmhyouzi.classList.add("d-none");
  carfmhyouzi.classList.add("d-none");
  byfmhyouzi.classList.add("d-none");
  mcfmhyouzi.classList.add("d-none");

  kensakumz.classList.add("d-none");

  //タイトル
  // forで回してd-none
  // [sougoumz, carmz, mcmz, bymz, kenkomz].forEach(element => {
  //   element.classList.add("d-none");});
  sougoumz.classList.add("d-none");
  carmz.classList.add("d-none");
  mcmz.classList.add("d-none");
  bymz.classList.add("d-none");
  kenkomz.classList.add("d-none");

  // 選択されたmobrityが絞り込みされていたら表示
  if(sentaku==mbb){
    kenkomz.classList.remove("d-none");
  }

  // 値がsougouならd-noneを除去で表示
  if(sentaku=="sougou"){
    sougoudbhyouzi.classList.remove("d-none");
    sougoufmhyouzi.classList.remove("d-none");
    kensakumz.classList.remove("d-none");
    sougoumz.classList.remove("d-none");
  };
  // carなら
  if(sentaku=="car"){
    cardbhyouzi.classList.remove("d-none");
    carfmhyouzi.classList.remove("d-none");
    carmz.classList.remove("d-none");
    // 商品名追加if(car)
    CARmn();
  };
  // mcなら
  if(sentaku=="mc"){
    mcdbhyouzi.classList.remove("d-none");
    mcfmhyouzi.classList.remove("d-none");
    mcmz.classList.remove("d-none");
    // 商品名追加if(mc)
    MCmn();
  };
  // byなら
  if(sentaku=="by"){
    bydbhyouzi.classList.remove("d-none");
    byfmhyouzi.classList.remove("d-none");
    bymz.classList.remove("d-none");
  };
  che()
};

// 製品の購入済み表示、非表示と価格ごと上か下
function che(){
  // 販売checkboxの状態を取得
  const hanbacheck=document.getElementById("hanbai_check");


  // なにを選択しているか取得する
  const mbs = document.getElementById("mbs");
  const sentaku = mbs.value; 
  // 今表示されているdb表示の外枠取得
  const ndbh = document.getElementById(sentaku + "dbhyouzi");

  //製品の状態を取得
  const zyoutai=ndbh.getElementsByClassName('zyoutai');

  // 当該製品を表示非表示のためのクラス取得。classnameでやると配列もどきのhtmlコレクションで取得される
  // HTMLCollection を配列に変換
  // 今表示されているdb内のzyoiを取得
  const zyoi = Array.from(ndbh.getElementsByClassName("zyoi"));


  // 製品全表示(前の処理で非表示説があるため)
  for (let i = 0; i< zyoi.length;i++){
    zyoi[i].classList.remove("d-none");
  }

  // 販売checkされているのなら出品状態ではない奴除外
  if (hanbacheck.checked){
    // for ループで回す
    for (let i = 0; i < zyoutai.length; i++) {
      // zyoutaiが1でない(出品中でない)
      if(zyoutai[i].textContent == "True"){
        // 非表示
        zyoi[i].classList.add("d-none");;
      };
    };
  };

  //価格表示
  // 選択されているラジオボタンを取得
  // どちらを取得しているかとる(nameがuesitaで取得されている方)
  const uesita = document.querySelector('input[name="uesita"]:checked');

  // ソート並べ替えしていくzyoi(各カード)から2つずつを比べて整列させる
  zyoi.sort((a, b) => {
    // 各商品の価格を price クラスから取得（テキスト内容）
    // priceaに入れてくださいねa(取得した2ずつのうちの一つ)のpriceクラスのテキストの中身を数値だけ(,や￥を除外)にして十進数整数にしたものを
    const priceA = parseInt(a.querySelector(".price").textContent.replace(/[^\d]/g, ""), 10);
    const priceB = parseInt(b.querySelector(".price").textContent.replace(/[^\d]/g, ""), 10);

    
    // priceAが数値でなければtrueの否定(soldoutの文字列は数値ではない)、つまり数値true,数値じゃないfalse
    const isANumber = !isNaN(priceA);
    const isBNumber = !isNaN(priceB);

    // 両方が数値の場合、昇順または降順で並べ替え
    if (isANumber && isBNumber) {
      // 条件式?真の時実行:偽の時実行
      // 
      //ソートでは負の値が返された時現状維持(a,b入れ替えない)、正だと入れ替える
      // 
      // 返してください、安い順が選択されているならa-bをしてください
      return uesita.value === "sitakara" ? priceA - priceB : priceB - priceA;
    }

    // 数値がある要素を前に、文字列のみの要素を後ろに配置
    // aが文字列だったら
    if (!isANumber && isBNumber) {
      // aを後ろにしたい(順番を変えたい)から正を返す
      return 1; // A が数値なし、B が数値 → A を後ろに
    }
    // bが文字列だったら
    if (isANumber && !isBNumber) {
      // 現状維持負
      return -1; // A が数値、B が数値なし → B を後ろに
    }

    // 両方が数値でない場合、順序を変えない
    return 0;
    });


    // 並べ替え後の商品をDOMに再配置する
    // zyoi一つひとつをitemとして親要素(各dbhyouzi)の中に入れる
    zyoi.forEach(item =>ndbh.appendChild(item)); 
  
}


//検索反映用mc
function MCmn(){
  const makerField = document.getElementById('mc_maker');
  const displacementField = document.getElementById('mc_displacement');
  const modelnameField = document.getElementById('mc_modelname');

  function updateModelNames() {
      const maker = makerField.value;
      const displacement = displacementField.value;

      if (maker && displacement) {
          fetch(`/load-MCmodelnames/?maker=${maker}&displacement=${displacement}`)
              .then(response => response.json())
              .then(data => {
                  modelnameField.innerHTML = '';
                  data.forEach(option => {
                      const opt = document.createElement('option');
                      opt.value = option.id;
                      opt.textContent = option.name;
                      modelnameField.appendChild(opt);
                  });
              });
      }
  }
// addeventlisnerは変わっても実行しつづける
makerField.addEventListener('change', updateModelNames);
displacementField.addEventListener('change', updateModelNames);
//初期値読み取って変えるよう変更
      // ページ読み込み時に初期値が存在すれば自動更新
      if (makerField && displacementField) {
        // もし既に値が設定されていれば更新を実行
        if (makerField.value && displacementField.value) {
            updateModelNames();
        }
    }

}

// 検索反映用car
function CARmn(){
  const makerField = document.getElementById('car_maker');
  const modelnameField = document.getElementById('car_modelname');

  function updateModelNames() {
      const maker = makerField.value;

      if (maker) {
          fetch(`/load-Cmodelnames/?maker=${maker}`)
              .then(response => response.json())
              .then(data => {
                  modelnameField.innerHTML = ''; // 既存の選択肢をクリア
                  data.forEach(option => {
                      const opt = document.createElement('option');
                      opt.value = option.id;
                      opt.textContent = option.name;
                      modelnameField.appendChild(opt);
                  });
              });
      }
  }

  makerField.addEventListener('change', updateModelNames);
  //初期値読み取って変えるよう変更
      // ページ読み込み時に初期値が存在すれば自動更新
      if (makerField ) {
        // もし既に値が設定されていれば更新を実行
        if (makerField.value ) {
            updateModelNames();
        }
    }
}
