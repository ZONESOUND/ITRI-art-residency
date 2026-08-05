/* Bilingual editorial revision for Rhythmic Entanglements prototype */
const revisedPages = [
  {
    n: 1,
    kind: "cover",
    zh: "節奏繞纏",
    en: "Rhythmic Entanglements",
    deck_zh: "讓差異可被感知的介面",
    deck_en: "Interfaces That Make Differences Perceptible",
    body_zh: "",
    body_en: "",
    caption_zh: "工研院藝術進駐衍生出版品",
    caption_en: "A publication developed through an artist residency at ITRI",
    note: "封面以中英文作品名與較精簡的出版品副標建立主題。英文不是逐字直譯，而是凸顯介面讓差異變得可感知。"
  },
  {
    n: 2,
    kind: "intro",
    zh: "我們如何感覺自己的身體，也留意另一個人的動作與回應？",
    en: "How Do We Sense Our Own Bodies and Attend to Another Person’s Movements and Responses?",
    body_zh: "《節奏繞纏》從心率、呼吸與動作等身體訊號的聲音化出發。透過原型測試、場域參訪與工作坊，研究逐漸連結感知差異、生活經驗與介面設計，並探問介面能否讓不同的身體經驗被表達、察覺與回應。",
    body_en: "Rhythmic Entanglements began with the sonification of bodily signals such as heart rate, breathing, and movement. Through prototypes, field visits, and workshops, the research connected sensory difference, lived experience, and interface design. It asks whether an interface can allow different bodily experiences to be expressed, noticed, and responded to.",
    caption_zh: "研究路徑：訊號 → 感知 → 差異 → 介面",
    caption_en: "Research path: signal → perception → difference → interface",
    note: "第 2 面提出整體問題。中文與英文各自成段，資訊對等，但英文不刻意複製中文語序。"
  },
  {
    n: 3,
    kind: "signals",
    zh: "從訊號到感知",
    en: "From Signals to Perception",
    body_zh: "心率、呼吸、移動、施力與觸碰，經過感測，被轉為聲音、影像與即時回饋。這些轉譯讓原本不易察覺的身體變化，可以被聽見、看見，或在操作中被感知。",
    body_en: "Heart rate, breathing, movement, force, and touch can be sensed and translated into sound, image, and real-time feedback. These translations make subtle bodily changes available to hearing, sight, and interaction.",
    caption_zh: "圖 1｜不同身體訊號與回饋方式之間的關係",
    caption_en: "Fig. 1 | Relations between bodily signals and forms of feedback",
    note: "第 3 面只處理訊號、轉譯與感知。圖示中的所有短標籤均改為中英對照。"
  },
  {
    n: 4,
    kind: "experience",
    zh: "相似的動作，帶著不同的經驗",
    en: "Similar Movements, Different Experiences",
    body_zh: "抓住、扶持、推動、旋轉、放開。這些看似簡單的手部動作，可能連著學習、工作、照顧、移動與記憶。即使動作相似，每個人所需的力量、熟悉程度，以及動作在生活中的意義，也不盡相同。",
    body_en: "Grasping, supporting, pushing, turning, and letting go may appear simple, yet they can be connected to learning, working, caring, moving, and remembering. Similar movements may require different degrees of strength and familiarity, and may carry different meanings in each person’s life.",
    caption_zh: "圖 2｜工作坊中的手勢、物件與生活片段",
    caption_en: "Fig. 2 | Gestures, objects, and fragments of everyday life from the workshops",
    note: "第 4 面的五個手勢均補上英文。英文正文保留生活經驗的差異，不簡化成動作詞列表。"
  },
  {
    n: 5,
    kind: "interface",
    zh: "介面如何容納不同的身體？",
    en: "How Can an Interface Make Room for Different Bodies?",
    body_zh: "相同的聲音、動作或觸碰，對不同的人可能形成不同的感受。透過調整感測靈敏度、回饋形式與反應節奏，介面不必要求所有人以相同方式操作，而能讓不同的感知方式、動作習慣與表達能力進入互動。",
    body_en: "The same sound, movement, or touch may be experienced differently by different people. By adjusting sensing sensitivity, forms of feedback, and response timing, an interface need not require everyone to interact in the same way. It can make room for different sensory modes, movement habits, and forms of expression.",
    caption_zh: "可調整的條件：速度、力量、靈敏度、反應節奏與回饋通道",
    caption_en: "Adjustable conditions: speed, force, sensitivity, response timing, and feedback channels",
    note: "將「回應不同的身體」改為「容納不同的身體」，避免暗示介面會自動辨識或代替使用者理解差異。"
  },
  {
    n: 6,
    kind: "device",
    zh: "同動車，如何成為可演奏的介面？",
    en: "How Can a Rehabilitation Device Become a Playable Interface?",
    body_zh: "同動車原本是一項雙手協調訓練裝置。研究加入移動、握力與敲擊感測，將方向、速度與施力轉化為聲音和影像，使原本用於訓練的裝置成為可以探索、演奏與回應的介面。呼吸與心率則透過其他原型，探索不同的身體聲音化路徑。",
    body_en: "Originally designed for bimanual coordination training, the device was extended with movement, grip, and tapping sensors. Direction, speed, and force are translated into sound and image, turning a rehabilitation device into an interface for exploration, performance, and response. Breathing and heart rate were explored through separate sonification prototypes.",
    caption_zh: "圖 3｜同動車的感測與回饋配置",
    caption_en: "Fig. 3 | Sensing and feedback configuration of the paired-motion device",
    note: "英文標題不硬譯「同動車」，而先以 rehabilitation device 說明其原始功能；正文再用 the device 或 paired-motion device。"
  },
  {
    n: 7,
    kind: "relation",
    zh: "當差異在介面中相遇",
    en: "When Differences Meet Through an Interface",
    body_zh: "當兩個人共用同動車，一個人的推動、停頓與施力，會成為另一個人可以察覺並回應的線索。兩人不必做出相同的動作，而是在速度、方向與力量之間持續等待、選擇與調整。共同操作不是目的，而是一種讓差異得以出現、被察覺並被回應的情境。",
    body_en: "When two people share the device, one person’s movement, pauses, and force become cues that the other can notice and respond to. They do not need to perform the same movements. Instead, they wait, choose, and adjust across differences in speed, direction, and force. Shared operation is not the goal itself, but a situation in which differences can emerge, become perceptible, and receive a response.",
    caption_zh: "帶領／跟隨　移動／停下　等待／回應　施力／放鬆",
    caption_en: "Leading / following · moving / pausing · waiting / responding · applying / releasing force",
    note: "第 7 面維持較具詩性的標題，但正文具體說明共同操作只是讓差異顯現與被回應的情境。"
  },
  {
    n: 8,
    kind: "back",
    zh: "相關實踐",
    en: "Related Practices",
    body_zh: "《節奏繞纏》延續融聲創意近年對共融音樂介面、感知差異與共同創作的探索。掃描 QR code，可閱讀本次計畫的技術資料、工作坊紀錄、影像與相關實踐。",
    body_en: "Rhythmic Entanglements continues Zone Sound Creative’s exploration of inclusive musical interfaces, sensory difference, and collaborative creation. Scan the QR code to access technical documentation, workshop records, video, and related practices.",
    caption_zh: "製作團隊／合作單位／補助單位／QR code",
    caption_en: "Credits / partners / funders / QR code",
    note: "封底正文與資訊標籤均提供中英文，QR 頁面可再承接完整技術與相關計畫資料。"
  }
];

revisedPages.forEach((item, index) => Object.assign(pages[index], item));

const originalVisual = visual;

slider = function (zh, en, leftZh, leftEn, rightZh, rightEn) {
  return `<div class="slider-row">
    <span><span class="zh-copy">${zh}</span><span class="en-copy">${en}</span></span>
    <div class="track"></div>
    <span><span class="zh-copy">${leftZh}／${rightZh}</span><span class="en-copy">${leftEn} / ${rightEn}</span></span>
  </div>`;
};

visual = function (kind) {
  if (kind === "signals") {
    return `<div class="signal-icons">
      ${icon("heart", "心率", "Heart Rate")}
      ${icon("breath", "呼吸", "Breathing")}
      ${icon("move", "移動", "Movement")}
      ${icon("force", "施力", "Force")}
      ${icon("touch", "觸碰", "Touch")}
    </div>
    <div class="arrow-down">↓</div>
    <div class="outputs">
      ${output("聲音", "Sound", "◖◗")}
      ${output("影像", "Image", "▣")}
      ${output("即時回饋", "Real-time Feedback", "↻")}
    </div>`;
  }

  if (kind === "experience") {
    const gestures = [
      ["抓住", "Grasp"],
      ["扶持", "Support"],
      ["推動", "Push"],
      ["旋轉", "Turn"],
      ["放開", "Let Go"]
    ];
    return `<div class="hands">${gestures.map(([zh, en]) => `
      <div class="hand-card">
        <div class="handmark"><i class="palm"></i><i class="finger f1"></i><i class="finger f2"></i><i class="finger f3"></i><i class="finger f4"></i><i class="finger f5"></i></div>
        <span><span class="zh-copy">${zh}</span><span class="en-copy">${en}</span></span>
      </div>`).join("")}</div>
      <svg style="position:absolute;left:2%;right:2%;bottom:8%;width:96%;height:55px" viewBox="0 0 240 60">
        <path d="M5 40C45 4 72 55 115 25S177 55 235 12" fill="none" stroke="#0f56d9" stroke-width="2" stroke-dasharray="7 6"/>
      </svg>`;
  }

  if (kind === "interface") {
    return `<div class="sliders">
      ${slider("速度", "Speed", "慢", "Slow", "快", "Fast")}
      ${slider("力量", "Force", "輕", "Light", "重", "Strong")}
      ${slider("靈敏度", "Sensitivity", "低", "Low", "高", "High")}
      ${slider("反應節奏", "Response Timing", "等待", "Delayed", "即時", "Immediate")}
    </div>
    <div class="modalities">
      <div class="mod"><span>◉</span><span class="zh-copy">聲音</span><span class="en-copy">Sound</span></div>
      <div class="mod"><span>▣</span><span class="zh-copy">影像</span><span class="en-copy">Image</span></div>
      <div class="mod"><span>≈</span><span class="zh-copy">觸覺</span><span class="en-copy">Tactile</span></div>
      <div class="mod"><span>↔</span><span class="zh-copy">動作</span><span class="en-copy">Movement</span></div>
    </div>`;
  }

  if (kind === "device") {
    return `<div class="device">
      <div class="cart"></div><div class="handle left"></div><div class="handle right"></div>
      <div class="grip g1"></div><div class="grip g2"></div><div class="xy"></div>
      <div class="piezo"><span class="zh-copy">敲擊</span><span class="en-copy">Tapping</span></div>
      <div class="chip ch1"><span class="zh-copy">握力</span><span class="en-copy">Grip Force</span></div>
      <div class="chip ch2"><span class="zh-copy">方向／速度</span><span class="en-copy">Direction / Speed</span></div>
      <div class="chip ch3"><span class="zh-copy">聲音＋影像</span><span class="en-copy">Sound + Image</span></div>
    </div>`;
  }

  if (kind === "relation") {
    return `<div class="relation">
      <div class="person left"><div class="head"></div><div class="torso"></div></div>
      <div class="person right"><div class="head"></div><div class="torso"></div></div>
      <div class="center-device"></div><div class="cue blue"></div><div class="cue red"></div><div class="cue dash"></div>
      <div class="relwords">
        <span><span class="zh-copy">帶領／跟隨</span><span class="en-copy">Leading / Following</span></span>
        <span><span class="zh-copy">等待／回應</span><span class="en-copy">Waiting / Responding</span></span>
      </div>
    </div>`;
  }

  return originalVisual(kind);
};

const bCallouts = [
  `<strong><span class="zh-copy">手部圖像</span><span class="en-copy">Hand Drawings</span></strong>
   <span class="zh-copy">五指承接不同的人生階段、物件或關係。</span>
   <span class="en-copy">Five fingers hold different stages of life, objects, and relationships.</span>`,
  `<strong><span class="zh-copy">片段話語</span><span class="en-copy">Fragments of Writing</span></strong>
   <span class="zh-copy">保留參與者的筆跡與用詞，而不是改寫成統一的人物傳記。</span>
   <span class="en-copy">Participants’ marks and words are retained rather than rewritten into uniform biographies.</span>`,
  `<strong><span class="zh-copy">形狀與感受</span><span class="en-copy">Shapes and Sensations</span></strong>
   <span class="zh-copy">圖形、顏色與身體經驗在同一張圖面上彼此交錯。</span>
   <span class="en-copy">Shapes, colors, and bodily experiences intersect across a shared visual field.</span>`,
  `<strong><span class="zh-copy">同一圖面，多重經驗</span><span class="en-copy">One Field, Multiple Experiences</span></strong>
   <span class="zh-copy">B 面不是八篇文章，而是一張由手部圖像、日常物件、形狀與片段文字交織而成的圖像場域。</span>
   <span class="en-copy">The reverse side is not a set of eight articles, but a visual field interweaving hand drawings, everyday objects, shapes, and fragments of writing.</span>`
];

document.querySelectorAll(".callout").forEach((el, index) => {
  el.innerHTML = bCallouts[index];
});

const aSheet = document.getElementById("aSheet");
aSheet.innerHTML = "";
pages.forEach((p) => {
  const panel = document.createElement("button");
  panel.className = `a-panel panel-${p.kind}`;
  panel.innerHTML = `<div class="mini-num">FACE ${p.n}</div>
    <h3 class="zh-title">${p.zh}</h3>
    <h4 class="en-title">${p.en}</h4>
    <div class="mini-visual">${visual(p.kind)}</div>
    <p class="zh-copy">${p.body_zh || p.deck_zh || ""}</p>
    <p class="en-copy">${p.body_en || p.deck_en || ""}</p>
    <div class="mini-cap"><span class="zh-copy">${p.caption_zh}</span><span class="en-copy">${p.caption_en}</span></div>`;
  panel.onclick = () => openModal(p);
  aSheet.appendChild(panel);
});

renderSpread(spreadIndex);
renderSingle(pageIndex);
