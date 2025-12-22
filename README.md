# **基於 Python 與 Streamlit 框架之互動式五大人格心理測驗平台開發與專題報告撰寫全方位指南**

## **1\. 緒論**

在當代資訊科學與心理學的跨領域應用中，將標準化的心理測驗（Psychological Assessment）數位化並部署為互動式網頁應用程式，已成為計算社會科學（Computational Social Science）的重要實踐方向。對於資訊工程或心理學背景的學生而言，開發一個自主設計的心理測驗網站，不僅是 Python 程式設計技能的綜合展現，更是對資料結構、演算法邏輯、使用者體驗（UX）設計以及領域知識（Domain Knowledge）整合的深度考驗。特別是在當前的教育評量趨勢中，強調「知識軌跡」的呈現，這要求開發者不僅要產出結果，更需記錄從問題發想到解決方案的完整歷程。

本報告旨在提供一份詳盡的實作指引與學術報告撰寫建議，協助讀者從零開始打造一個具備科學效度與高度互動性的心理測驗平台。本報告將分為六大核心章節：首先探討心理測驗的理論基礎與量表選擇，確保測驗的科學性；其次深入分析技術架構的決策過程，特別是 Streamlit 與 Flask 的框架評估；第三部分將詳細解構系統實作細節，涵蓋計分演算法、狀態管理與視覺化工程；第四部分將結合現代 AI 技術，探討如何整合大型語言模型（LLM）以提供個人化回饋，回應「跨域創新」的評分指標；第五部分則聚焦於專題報告的撰寫策略，依據學術規範詳細解析各章節的撰寫要點，並針對「知識軌跡」的紀錄提供具體建議；最後則總結專案價值與未來展望。

透過本報告的系統性引導，讀者將能夠理解如何將抽象的心理學構念轉化為具體的程式邏輯，並最終以嚴謹的學術格式呈現研究成果，完成一份兼具實用性、創新性與學術價值的專題報告。

## ---

**2\. 心理計量學基礎與測驗量表選型**

在編寫任何程式碼之前，必須先確立測驗的「內容效度」（Content Validity）。一個專業的心理測驗網站不同於社交媒體上常見的娛樂性質測驗，其核心價值在於背後的量表是否經過科學驗證，以及計分邏輯是否符合心理計量學（Psychometrics）的標準。

### **2.1 測驗模型的理論選擇：五大人格特質 vs. MBTI**

在心理學領域中，人格測驗的模型選擇直接決定了系統的資料結構與演算法設計。目前最廣為人知的兩種模型為 MBTI（Myers-Briggs Type Indicator）與五大人格特質（Big Five Personality Traits，又稱 OCEAN 模型）。

#### **2.1.1 模型比較分析**

| 比較維度 | 五大人格特質 (Big Five/OCEAN) | MBTI (Myers-Briggs Type Indicator) |
| :---- | :---- | :---- |
| **理論基礎** | 基於詞彙學假設（Lexical Hypothesis），經由因素分析（Factor Analysis）統計歸納而來 1。 | 基於榮格（Carl Jung）的心理類型理論，屬於類型學派（Typology）。 |
| **評分方式** | **維度論（Dimensional）**：每個特質都是一個連續光譜，個體落在光譜的某一點（如：外向性 PR 75）。 | **類型論（Categorical）**：將人二分法歸類（如：E vs. I），忽視中間值的個體差異。 |
| **信度與效度** | 具有高度的重測信度（Test-Retest Reliability）與預測效度，廣泛應用於學術研究與臨床評估 2。 | 爭議較多，部分研究顯示重測信度不穩定，學術界接受度較低 3。 |
| **資料特性** | 數值型資料（Continuous/Interval），適合進行迴歸分析、雷達圖繪製與精細比較。 | 類別型資料（Nominal/Ordinal），適合簡單分類，但在數據分析上受限較多。 |
| **適用場景** | 學術研究、深度的自我探索、職涯適性分析。 | 企業破冰活動、初步的人際風格了解、娛樂性較高。 |

基於專題報告要求「跨域創新」與「內容正確」的評分標準，本報告強烈建議採用 **五大人格特質模型**。該模型將人格分為五個主要維度：開放性（Openness）、盡責性（Conscientiousness）、外向性（Extraversion）、親和性（Agreeableness）與神經質（Neuroticism）。這五個維度提供了豐富的數據點，非常適合用 Python 進行資料分析與 Matplotlib 雷達圖的繪製，能充分展現程式技術與心理學理論的結合 4。

### **2.2 量表來源：國際人格題項庫 (IPIP)**

為了避免使用商業量表（如 NEO-PI-R）可能引發的版權爭議，並符合學術專題的開源精神，本專案應採用 **國際人格題項庫（International Personality Item Pool, IPIP）** 2。IPIP 是一個由學術界共同維護的公有領域題庫，其量表與商業量表具有高度的相關性，但完全免費且開放使用。

在 IPIP 的眾多版本中，**IPIP-NEO-120** 是最適合學生專題的選擇 5：

* **IPIP-NEO-300**：包含 300 題，雖然精確度最高，但測驗時間過長（約 30-40 分鐘），容易導致網頁使用者產生疲勞效應（Fatigue Effect），影響數據品質與使用者體驗。  
* **IPIP-NEO-120**：精簡至 120 題，每個維度 24 題，既保留了足夠的信度（Cronbach's $\\alpha$ 通常大於 0.80），又能將測驗時間控制在 15 分鐘以內，是網頁應用的最佳平衡點。  
* **Mini-IPIP**：僅 20 或 50 題，雖然快速，但在細維度（Facets）的分析上較為粗糙，難以支撐深度報告所需的數據分析 1。

### **2.3 心理計量學的關鍵邏輯：反向計分 (Reverse Keying)**

在程式實作階段，最容易被忽視但卻至關重要的邏輯是「反向計分」。這是心理測驗為了防止「默許偏差」（Acquiescence Bias，即受測者傾向於不假思索地同意所有題目）而設計的機制 7。

#### **2.3.1 正向題與反向題的定義**

* **正向題（Positively Keyed）**：題目的敘述方向與該特質的高分方向一致。  
  * *範例*：「我是聚會的靈魂人物。」（測量外向性）  
  * *計分*：若受測者選「5 分（非常同意）」，則該題得分為 5 分。  
* **反向題（Negatively Keyed）**：題目的敘述方向與該特質的高分方向相反。  
  * *範例*：「我不喜歡在人多的場合說話。」（測量外向性）  
  * *計分*：若受測者選「5 分（非常同意）」，代表其外向性極低，因此該題的實際得分應轉化為低分。

#### **2.3.2 轉換演算法**

對於採用 Likert 5 點量表（1=非常不同意, 5=非常同意）的測驗，反向計分的轉換公式為：

$$S\_{transformed} \= (Max \+ Min) \- S\_{raw}$$

代入 5 點量表，即：

$$S\_{transformed} \= 6 \- S\_{raw}$$

例如，若使用者在反向題選了 5 分，實際得分為 $6 \- 5 \= 1$ 分；若選了 2 分，實際得分為 $6 \- 2 \= 4$ 分。  
在系統設計時，必須在題庫資料結構（如 JSON 或 Database）中明確標記每一題的計分方向（Keyed Direction），並在後端演算法中實作此轉換邏輯，否則算出的結果將完全錯誤，這將直接影響報告中「內容正確」維度的評分 2。

## ---

**3\. 技術架構決策與系統設計**

在確立了心理學理論基礎後，下一步是選擇合適的技術堆疊（Tech Stack）。對於本專題而言，Python 是無可爭議的首選語言，因為其擁有強大的資料處理（Pandas）、科學計算（NumPy）與視覺化（Matplotlib/Plotly）生態系 8。然而，在 Web 框架的選擇上，開發者往往面臨 **Flask** 與 **Streamlit** 的抉擇。

### **3.1 Web 框架評估：Flask vs. Streamlit**

為了在有限的學期時間內完成高品質的專題，必須根據專案需求進行技術取捨。以下依據文獻 10 進行深度比較分析：

| 比較維度 | Flask (微框架) | Streamlit (資料應用框架) | 專題適用性分析 |
| :---- | :---- | :---- | :---- |
| **核心定位** | 用於構建通用的 Web 後端與 API，提供極高的靈活性與控制權。 | 專為數據科學家設計，用於快速將 Python 腳本轉化為互動式 Web UI。 | Streamlit 更適合本專題，因為重點在於「數據分析」而非「網頁開發」。 |
| **前端開發需求** | **極高**：需自行編寫 HTML、CSS、JavaScript，並處理 Jinja2 模板渲染與 AJAX 資料交換。 | **極低**：完全使用 Python 語法（如 st.radio, st.button）生成前端元件，無需接觸 HTML/CSS。 | Flask 會分散開發者精力於前端除錯；Streamlit 則能專注於計分邏輯。 |
| **開發速度** | 較慢：需配置路由（Routing）、請求處理（Request Handling）與資料庫連結。 | **極快**：數行程式碼即可生成可運作的原型（Prototype），大幅縮短開發週期。 | Streamlit 能在短時間內產出具備完整功能的成品，有利於期末展示。 |
| **狀態管理** | 無狀態（Stateless），需自行實作 Session 或 Cookie 機制來傳遞變數。 | 內建 st.session\_state 機制，能直觀地在不同互動間傳遞變數（如頁碼、答案）。 | Streamlit 的 Session State 對於多頁式問卷（Multi-page Survey）非常友善 13。 |
| **資料視覺化** | 需將圖表存為圖片檔傳輸，或整合前端圖表庫（如 Chart.js），整合度較低。 | 與 Matplotlib、Plotly 高度整合，僅需一行 st.pyplot() 即可顯示互動式圖表。 | 這是本專題的核心亮點，Streamlit 在此方面具有壓倒性優勢 14。 |

**決策結論**：考量到專題評分重點在於「Python 應用實作」與「知識軌跡」，而非前端網頁切版技術，本報告強烈建議採用 **Streamlit**。它能讓開發者將 80% 的時間投入在核心的計分演算法、資料分析與視覺化呈現上，從而產出更具深度的報告內容，而非僅是一個外觀精美但功能單薄的網頁 15。

### **3.2 系統架構設計 (System Architecture)**

基於 Streamlit 的特性，我們採用「單頁應用多視圖」（Single Page App with Multi-Views）的架構模式。系統可分為三個主要層次 16：

#### **3.2.1 前端互動層 (Frontend Layer)**

* **輸入介面**：利用 st.radio 生成單選題組，並使用 st.form 將每一頁的題目包裹起來，避免使用者每點擊一個選項就觸發頁面重整（Rerun），改善使用者體驗 19。  
* **導航控制**：利用 st.progress 顯示作答進度，並提供「上一頁」、「下一頁」按鈕。  
* **結果展示**：利用 st.pyplot 或 st.plotly\_chart 呈現雷達圖，並使用 st.expander 提供詳細的文字解釋。

#### **3.2.2 業務邏輯層 (Logic Layer)**

* **狀態管理器 (State Manager)**：利用 st.session\_state 追蹤使用者的當前狀態，包括：  
  * current\_page: 當前所在的頁碼。  
  * answers: 一個字典（Dictionary），鍵為題目 ID，值為使用者的原始評分（1-5）。  
  * submission\_status: 標記是否已完成測驗。  
* **計分引擎 (Scoring Engine)**：負責讀取題庫資料，執行反向計分轉換，並聚合五大特質的得分 7。  
* **AI 整合模組 (AI Integration)**：若需達到「跨域創新」的高分標準，可在此層整合 OpenAI API，將計算出的五大特質分數轉化為 Prompt，生成個人化的性格分析報告 21。

#### **3.2.3 資料持久層 (Data Layer)**

* **靜態題庫**：使用 JSON 檔案（questions.json）儲存 IPIP-120 的題目資料，包含題目 ID、文字內容、所屬維度、正反向標記等。這體現了「資料與邏輯分離」的軟體工程原則 22。  
* **動態記錄**：若有進階需求，可整合 SQLite 或 CSV 檔案，將使用者的測驗結果（匿名化）持久化儲存，以便後續進行群體資料分析（如：全班的人格常模分佈）23。

### **3.3 資料庫模型設計 (Database Schema)**

雖然 Streamlit 應用可以不依賴外部資料庫運行，但為了體現專題的完整性與資料分析潛力，建議設計一個輕量級的資料結構。以下為基於 JSON 或 NoSQL 文檔結構的設計範例 25：

| 欄位名稱 | 資料型態 | 說明 |
| :---- | :---- | :---- |
| user\_id | String (UUID) | 匿名使用者的唯一識別碼。 |
| timestamp | DateTime | 測驗完成時間。 |
| raw\_responses | Dictionary | 儲存原始答題數據，如 {"q1": 5, "q2": 2,...}。 |
| scores | Dictionary | 儲存計算後的維度得分，如 {"Openness": 3.8, "Conscientiousness": 4.2,...}。 |
| ai\_feedback | String | (Optional) 若有整合 AI，儲存 AI 生成的文字評語。 |

這樣的設計不僅能滿足當下的測驗需求，也為未來的數據挖掘（如分析某個維度的平均分數趨勢）保留了可能性，這在報告的「未來展望」章節中是一個極佳的論述點。

## ---

**4\. 系統實作細節與程式碼解析**

本章節將深入探討核心功能的程式碼實作，包括環境建置、題庫載入、狀態管理、計分邏輯與視覺化工程。這些程式碼片段可直接應用於專題報告的「實作過程」章節，展示技術深度。

### **4.1 開發環境配置**

首先，建立專案資料夾並配置必要的 Python 套件。建議使用虛擬環境（Virtual Environment）以確保依賴管理的乾淨與可移植性。

Bash

\# 建立並啟用虛擬環境  
python \-m venv venv  
source venv/bin/activate  \# Windows: venv\\Scripts\\activate

\# 安裝核心套件  
pip install streamlit pandas matplotlib plotly numpy openai

* streamlit: 應用程式主框架。  
* pandas: 用於處理題庫資料結構與計算統計數據。  
* numpy: 用於雷達圖的角度計算與數值處理。  
* matplotlib: 產生靜態雷達圖，適合報告截圖。  
* openai: (選用) 用於串接 GPT 模型生成個人化分析。

### **4.2 題庫資料結構實作 (questions.json)**

將題目硬編碼（Hard-coding）在程式中是軟體開發的大忌。應將題目抽離為獨立的 JSON 檔案，這不僅便於維護，也方便未來替換不同語言或版本的量表 22。

JSON

\[  
  {  
    "id": 1,  
    "question": "我在聚會中通常是焦點人物。",  
    "trait": "Extraversion",  
    "keyed": "plus"  
  },  
  {  
    "id": 2,  
    "question": "我不太關心別人的問題。",  
    "trait": "Agreeableness",  
    "keyed": "minus"   
  },  
 ...  
\]

在此結構中，keyed: minus 明確指示了該題需要進行反向計分運算。

### **4.3 Streamlit 狀態管理與分頁邏輯**

Streamlit 的 st.session\_state 是實現多頁問卷的核心。由於 Streamlit 採用宣告式語法（Declarative Syntax），每次使用者互動都會導致整個腳本從頭執行，因此必須利用 Session State 來「記住」使用者的進度 13。

Python

import streamlit as st  
import json

\# 1\. 初始化 Session State  
if 'answers' not in st.session\_state:  
    st.session\_state\['answers'\] \= {}  \# 儲存 {question\_id: score}  
if 'current\_page' not in st.session\_state:  
    st.session\_state\['current\_page'\] \= 0 \# 當前頁碼 (例如每頁10題)

\# 2\. 載入題目資料  
@st.cache\_data  \# 使用快取裝飾器優化效能  
def load\_questions():  
    with open('questions.json', 'r', encoding='utf-8') as f:  
        return json.load(f)

questions \= load\_questions()  
QUESTIONS\_PER\_PAGE \= 10

\# 3\. 分頁邏輯控制  
start\_idx \= st.session\_state\['current\_page'\] \* QUESTIONS\_PER\_PAGE  
end\_idx \= start\_idx \+ QUESTIONS\_PER\_PAGE  
page\_questions \= questions\[start\_idx:end\_idx\]

\# 4\. 介面渲染  
st.title("五大人格心理測驗")  
progress\_bar \= st.progress(st.session\_state\['current\_page'\] / (len(questions)/QUESTIONS\_PER\_PAGE))

\# 使用 Form 容器包裹題目，避免每點擊一題就觸發 Rerun  
with st.form(key=f'page\_form\_{st.session\_state\["current\_page"\]}'):  
    for q in page\_questions:  
        st.write(f"\*\*Q{q\['id'\]}.\*\* {q\['question'\]}")  
        \# 選項映射: 1=非常不同意... 5=非常同意  
        \# 注意: key 必須唯一，否則會報錯 DuplicateWidgetID  
        st.radio(  
            "請選擇符合程度:",   
            options=,   
            horizontal=True,  
            key=f"q\_{q\['id'\]}"   
        )  
        st.divider()  
          
    submit\_button \= st.form\_submit\_button(label="下一頁" if end\_idx \< len(questions) else "提交結果")

    if submit\_button:  
        \# 儲存當前頁面的答案到 Session State  
        for q in page\_questions:  
            \# 從 widget key 獲取使用者選擇  
            response \= st.session\_state.get(f"q\_{q\['id'\]}")  
            if response:  
                st.session\_state\['answers'\]\[str(q\['id'\])\] \= response  
          
        \# 頁面跳轉邏輯  
        if end\_idx \< len(questions):  
            st.session\_state\['current\_page'\] \+= 1  
            st.rerun() \# 強制重整以顯示下一頁  
        else:  
            st.session\_state\['finished'\] \= True  
            st.rerun()

### **4.4 核心計分演算法 (Scoring Algorithm)**

當使用者完成所有題目後，系統需執行計分運算。此函式展現了資料處理的邏輯能力，是報告中的技術亮點 2。

Python

def calculate\_big\_five\_scores(answers, questions\_db):  
    \# 初始化分數累積器  
    scores \= {"Extraversion": 0, "Agreeableness": 0, "Conscientiousness": 0, "Neuroticism": 0, "Openness": 0}  
    counts \= {"Extraversion": 0, "Agreeableness": 0, "Conscientiousness": 0, "Neuroticism": 0, "Openness": 0}  
      
    for q in questions\_db:  
        qid \= str(q\['id'\])  
        user\_response \= answers.get(qid)  
          
        if user\_response:  
            final\_score \= user\_response  
              
            \# 關鍵邏輯: 反向計分處理  
            if q\['keyed'\] \== 'minus':  
                final\_score \= 6 \- user\_response  
              
            \# 累積得分  
            scores\[q\['trait'\]\] \+= final\_score  
            counts\[q\['trait'\]\] \+= 1  
              
    \# 計算平均分 (Mean Score)  
    final\_results \= {}  
    for trait in scores:  
        if counts\[trait\] \> 0:  
            final\_results\[trait\] \= round(scores\[trait\] / counts\[trait\], 2)  
        else:  
            final\_results\[trait\] \= 0  
              
    return final\_results

### **4.5 視覺化工程：雷達圖繪製 (Radar Chart Visualization)**

心理測驗結果最經典的呈現方式是雷達圖。雖然 Matplotlib 支援極座標繪圖，但要畫出專業的封閉多邊形需要一定的數學處理技巧 29。

#### **數學原理**

雷達圖本質上是將多維數據映射到極座標系 $(r, \\theta)$ 上。

* **半徑 ($r$)**：代表特質的得分（例如 1-5 分）。  
* **角度 ($\\theta$)**：將 $2\\pi$（360度）平均分配給 $N$ 個維度。對於五大人格，每個軸的角度間隔為 $72^\\circ$（$2\\pi / 5$）。  
* **封閉性**：為了讓線條閉合，數據點序列的最後必須重複第一個點的值，角度序列也需同樣處理。

Python

import numpy as np  
import matplotlib.pyplot as plt

def plot\_radar\_chart(scores):  
    \# 準備數據  
    categories \= list(scores.keys())  
    values \= list(scores.values())  
      
    \# 數據閉合處理  
    values \+= values\[:1\]  
      
    \# 計算角度 (將圓周等分)  
    angles \= \[n / float(len(categories)) \* 2 \* np.pi for n in range(len(categories))\]  
    angles \+= angles\[:1\]  
      
    \# 初始化極座標圖表  
    fig, ax \= plt.subplots(figsize=(6, 6), subplot\_kw=dict(polar=True))  
      
    \# 設定起始角度 (讓第一個軸朝正上方)  
    ax.set\_theta\_offset(np.pi / 2)  
    ax.set\_theta\_direction(-1) \# 順時針方向  
      
    \# 繪製標籤  
    plt.xticks(angles\[:-1\], categories)  
      
    \# 繪製數據線與填充  
    ax.plot(angles, values, linewidth=2, linestyle='solid', color='\#FF4B4B')  
    ax.fill(angles, values, '\#FF4B4B', alpha=0.25)  
      
    \# 設定半徑刻度  
    plt.yticks(, \["1", "2", "3", "4", "5"\], color="grey", size=8)  
    plt.ylim(0, 5)  
      
    return fig

此段程式碼不僅展示了對 matplotlib 的掌握，更體現了對資料視覺化原理的理解，應在報告中詳細說明每一步驟的數學意義。

### **4.6 進階功能：整合 LLM 實現「跨域創新」**

為了在「跨域創新」評分項目中獲得滿分，強烈建議整合 OpenAI API（或本地 LLM），提供傳統測驗無法做到的「語義化回饋」。

* **實作概念**：將計算出的五個分數構建成一個 Prompt，傳送給 GPT 模型。  
* **Prompt 設計**："使用者在五大人格測驗的得分如下：開放性 4.5，盡責性 2.1，...。請以職業諮詢師的角度，分析其性格優勢與潛在盲點，並建議適合的職業發展方向。語氣請保持專業且具同理心，字數約 300 字。"  
* **報告論述**：這展示了如何將「結構化數據」（分數）轉化為「非結構化洞察」（自然語言建議），是 AI 時代心理測驗的演進方向 21。

## ---

**5\. 專題報告撰寫策略與格式規範**

技術實作完成後，如何將過程轉化為符合學術規範的報告是另一個挑戰。依據使用者提供的 31 專題報告格式說明 以及 32 評分標準，本節將提供嚴格的撰寫指引。

### **5.1 評分標準對應策略 (Rubric Alignment)**

在撰寫報告時，必須時刻對照評分標準，確保每個維度都有充分的內容支撐。

| 評分向度 | 評分重點 | 報告撰寫策略 |
| :---- | :---- | :---- |
| **跨域創新 (Innovation)** | 內容豐富多元，條列式說明。 | 強調「資訊技術」與「心理學」的結合。特別是 **AI 個人化回饋** 與 **互動式雷達圖** 的實作，應設專章說明。 |
| **內容完整 (Completeness)** | 正確且深入，確實標示重點。 | 必須包含完整的**系統流程圖**、**資料庫 Schema**、**核心演算法程式碼**。結構應涵蓋前言、方法、結果至結論。 |
| **內容正確 (Correctness)** | 完全正確。 | 確保 **反向計分邏輯** 無誤，並在文中引用 IPIP 相關文獻 5 佐證量表的科學性。避免使用錯誤的術語（如將五大特質混淆為 MBTI）。 |
| **圖表表現 (Charts)** | 運用圖表分析，完整呈現架構。 | 使用 Matplotlib 產生的雷達圖、draw.io 繪製的系統架構圖。圖表必須有編號與標題（Caption）。 |
| **版面編排 (Layout)** | 清晰，圖文並茂，架構完整。 | 嚴格遵守 31 的格式要求（字型、邊距、縮排）。 |

### **5.2 「知識軌跡」的紀錄與呈現 (Knowledge Trajectory)**

使用者的查詢中特別提到：「老師會根據...myGPTs的使用情況...看出『知識軌跡』」。這意味著**過程比結果更重要**。報告中必須有一個章節專門呈現「如何利用 AI 輔助開發」。

撰寫建議：  
在報告的「系統實作」或獨立章節中，加入「開發歷程與 AI 協作紀錄」：

1. **問題定義階段**：展示如何詢問 AI 關於「Python 心理測驗庫推薦」，並根據 AI 建議選擇 Streamlit 與 IPIP-NEO 的過程。  
2. **除錯階段 (Debugging)**：截圖或引用與 GPT 的對話，例如「如何解決 Streamlit 按鈕點擊後變數重置的問題？」。這證明了你理解 Session State 的概念是透過主動學習獲得的。  
3. **優化階段**：展示如何請 AI 優化雷達圖的配色或 Prompt 的設計。

**關鍵論述**：強調 AI 不是「代寫」工具，而是「結對程式設計師」（Pair Programmer）。你在與 AI 的互動中，展現了批判性思考（Critical Thinking）——例如 AI 給出的某些代碼無法運行，你是如何修正它的。這種「人機協作」的過程正是老師希望看到的「知識軌跡」。

### **5.3 格式規範檢核 (Format Checklist)**

依據 31，以下格式必須嚴格執行：

1. **版面設定**：  
   * **紙張**：A4 (21 × 29.7 cm)。  
   * **邊距**：上下 2.54 cm，左右 1.91 cm。**注意**：這與 Word 預設值不同，務必手動調整。  
   * **內容範圍**：所有圖表、頁碼不得超出邊界。  
2. **字型與段落**：  
   * **中文字型**：標楷體 (BiauKai)。  
   * **英文字型**：Times New Roman。  
   * **字級**：第一層標題 14pt 粗體；正文 12pt；摘要標題 12pt 粗體。  
   * **行距**：單行行距 (Single Spacing)。  
   * **縮排**：每一段落首行縮排 0.63 cm (0.25 inch)。  
   * **間距**：段落之間 **不可空行** (Do not add blank lines between paragraphs)。這是常見扣分點。  
3. **標題編號**：  
   * 第一層：1. 前言 (數字後加點)。  
   * 第二層：2.1. 研究背景 (數字後加點)。  
4. **圖表格式**：  
   * 圖片標題置於 **圖片下方**，置中。例如：Figure 1\. 系統架構流程圖。  
   * 表格標題置於 **表格上方**，置中。  
   * 圖表必須與內文有連結（Cross-reference），例如內文需提到「如 Figure 1 所示...」。

### **5.4 參考文獻規範 (References)**

引用必須遵循 APA 格式。

* **中文文獻**：按作者姓氏筆畫排序。  
* **英文文獻**：按作者姓氏字母排序。  
* **範例**：  
  * Goldberg, L. R. (1992). The development of markers for the Big-Five factor structure. *Psychological Assessment*, 4(1), 26–42.  
  * Streamlit Inc. (2023). *Streamlit documentation*. Retrieved from [https://docs.streamlit.io](https://docs.streamlit.io)  
  * 2 NeuroQuestAi. (2023). *five-factor-e: Big Five personality test in Python*. GitHub Repository.

## ---

**6\. 結論與未來展望**

本專案成功整合了心理計量學的理論基礎與現代化的 Web 開發技術，建置了一套具備科學效度與良好互動體驗的心理測驗平台。透過 Streamlit 框架的高效開發能力，我們得以將重心聚焦於核心的計分演算法與資料視覺化呈現，並透過 IPIP-NEO-120 量表確保了測驗內容的專業性。

在技術實作層面，本專案解決了多頁應用的狀態管理難題，並利用 Matplotlib 實現了動態雷達圖的繪製，成功將抽象的人格數據轉化為直觀的視覺圖表。此外，藉由整合大型語言模型（LLM），系統能夠提供具備語義理解能力的個人化建議，體現了跨領域技術融合的創新價值。

未來，本系統可進一步朝向「數據驅動」的方向發展。例如，透過引入 SQLite 資料庫長期累積使用者數據，建立屬於特定群體（如大學生）的常模（Norms），進而計算出更精確的百分位數（PR值）；或結合機器學習演算法，探索人格特質與其他行為變數（如學業表現）之間的關聯性。這將使本專題從單純的「工具開發」昇華為具備深度的「實證研究」，為計算心理學的應用提供更多可能性。

#### **引用的著作**

1. Big Five Personality Test \- Open Source Psychometrics Project, 檢索日期：12月 19, 2025， [http://openpsychometrics.org/tests/IPIP-BFFM/](http://openpsychometrics.org/tests/IPIP-BFFM/)  
2. NeuroQuestAi/five-factor-e: Python Library with a self-administered questionnaire that assesses a person's personality according to the Big Five model , using the IPIP-NEO. \- GitHub, 檢索日期：12月 19, 2025， [https://github.com/NeuroQuestAi/five-factor-e](https://github.com/NeuroQuestAi/five-factor-e)  
3. Open Source Psychometrics Project: Take a personality test, 檢索日期：12月 19, 2025， [http://openpsychometrics.org/](http://openpsychometrics.org/)  
4. Exploratory Data Analysis of Big Five Personality Test | by Kalluri Vasanthasai | Medium, 檢索日期：12月 19, 2025， [https://medium.com/@vasanthsai/exploratory-data-analysis-of-big-five-personality-test-c7b3e0d7d102](https://medium.com/@vasanthsai/exploratory-data-analysis-of-big-five-personality-test-c7b3e0d7d102)  
5. IPIP-NEO-120 \- International Personality Item Pool \- NovoPsych, 檢索日期：12月 19, 2025， [https://novopsych.com/assessments/formulation/international-personality-item-pool-neo-120-item-version-ipip-neo-120/](https://novopsych.com/assessments/formulation/international-personality-item-pool-neo-120-item-version-ipip-neo-120/)  
6. IPIP-NEO \- Big Five Personality, 120-Item Original \- Kaggle, 檢索日期：12月 19, 2025， [https://www.kaggle.com/datasets/edersoncorbari/ipip-neo-big-five-personality-120-item-original](https://www.kaggle.com/datasets/edersoncorbari/ipip-neo-big-five-personality-120-item-original)  
7. Scoring the Big Five Personality Test items \- Kaggle, 檢索日期：12月 19, 2025， [https://www.kaggle.com/code/bluewizard/scoring-the-big-five-personality-test-items](https://www.kaggle.com/code/bluewizard/scoring-the-big-five-personality-test-items)  
8. Psychology | Python across all Disciplines, 檢索日期：12月 19, 2025， [https://docs.pyclubs.org/python-across-all-disciplines/disciplines/psychology](https://docs.pyclubs.org/python-across-all-disciplines/disciplines/psychology)  
9. Python for Analytics and Assessment \- IOPsychology \- Reddit, 檢索日期：12月 19, 2025， [https://www.reddit.com/r/IOPsychology/comments/rwf8v3/python\_for\_analytics\_and\_assessment/](https://www.reddit.com/r/IOPsychology/comments/rwf8v3/python_for_analytics_and_assessment/)  
10. The Conclusive Face-Off: Flask vs Streamlit | by Soma Bhadra | Medium, 檢索日期：12月 19, 2025， [https://somabhadra.medium.com/the-conclusive-face-off-flask-vs-streamlit-40bdef6859a4](https://somabhadra.medium.com/the-conclusive-face-off-flask-vs-streamlit-40bdef6859a4)  
11. Flask vs Streamlit Comparison for Building Python Apps \- NunarIQ, 檢索日期：12月 19, 2025， [https://www.nunariq.com/knowledgebase/flask-vs-streamlit/](https://www.nunariq.com/knowledgebase/flask-vs-streamlit/)  
12. Do you think it's worth learning Streamlit? Or should one stick to Flask or Django? : r/Python, 檢索日期：12月 19, 2025， [https://www.reddit.com/r/Python/comments/ynzbre/do\_you\_think\_its\_worth\_learning\_streamlit\_or/](https://www.reddit.com/r/Python/comments/ynzbre/do_you_think_its_worth_learning_streamlit_or/)  
13. A Streamlit Quizz Template. A Simple Guide to Building a Quiz App… | by Hugoalmeidamoreira | Medium, 檢索日期：12月 19, 2025， [https://medium.com/@hugoalmeidamoreira/a-streamlit-quizz-template-505ae87c387f](https://medium.com/@hugoalmeidamoreira/a-streamlit-quizz-template-505ae87c387f)  
14. Chart elements \- Streamlit Docs, 檢索日期：12月 19, 2025， [https://docs.streamlit.io/develop/api-reference/charts](https://docs.streamlit.io/develop/api-reference/charts)  
15. Flask vs Streamlit to convert a desktop app to a web app : r/Python \- Reddit, 檢索日期：12月 19, 2025， [https://www.reddit.com/r/Python/comments/slqkcs/flask\_vs\_streamlit\_to\_convert\_a\_desktop\_app\_to\_a/](https://www.reddit.com/r/Python/comments/slqkcs/flask_vs_streamlit_to_convert_a_desktop_app_to_a/)  
16. kevinknights29/Introduction\_to\_AI\_Streamlit\_Quiz\_App: This project aims to build a quiz application using streamlit for the session: \`Introduction to AI\` \- GitHub, 檢索日期：12月 19, 2025， [https://github.com/kevinknights29/Introduction\_to\_AI\_Streamlit\_Quiz\_App](https://github.com/kevinknights29/Introduction_to_AI_Streamlit_Quiz_App)  
17. Overall architecture diagram of psychological assessment \- ResearchGate, 檢索日期：12月 19, 2025， [https://www.researchgate.net/figure/Overall-architecture-diagram-of-psychological-assessment\_fig1\_388850732](https://www.researchgate.net/figure/Overall-architecture-diagram-of-psychological-assessment_fig1_388850732)  
18. Understanding Streamlit's client-server architecture, 檢索日期：12月 19, 2025， [https://docs.streamlit.io/develop/concepts/architecture/architecture](https://docs.streamlit.io/develop/concepts/architecture/architecture)  
19. Web app in Streamlit with multiple questions per page \- Stack Overflow, 檢索日期：12月 19, 2025， [https://stackoverflow.com/questions/71316814/web-app-in-streamlit-with-multiple-questions-per-page](https://stackoverflow.com/questions/71316814/web-app-in-streamlit-with-multiple-questions-per-page)  
20. Session State \- Streamlit Docs, 檢索日期：12月 19, 2025， [https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session\_state](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)  
21. Build a basic LLM chat app \- Streamlit Docs, 檢索日期：12月 19, 2025， [https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps)  
22. five-factor-e/data/IPIP-NEO/120/questions.json at main \- GitHub, 檢索日期：12月 19, 2025， [https://github.com/NeuroQuestAi/five-factor-e/blob/main/data/IPIP-NEO/120/questions.json](https://github.com/NeuroQuestAi/five-factor-e/blob/main/data/IPIP-NEO/120/questions.json)  
23. Saving data from users into a CSV file \- Using Streamlit, 檢索日期：12月 19, 2025， [https://discuss.streamlit.io/t/saving-data-from-users-into-a-csv-file/20245](https://discuss.streamlit.io/t/saving-data-from-users-into-a-csv-file/20245)  
24. Streamlit save user data and update CSV \- python \- Stack Overflow, 檢索日期：12月 19, 2025， [https://stackoverflow.com/questions/74731511/streamlit-save-user-data-and-update-csv](https://stackoverflow.com/questions/74731511/streamlit-save-user-data-and-update-csv)  
25. Personality Database Structure and Schema Diagram, 檢索日期：12月 19, 2025， [https://databasesample.com/database/personality-database](https://databasesample.com/database/personality-database)  
26. Free open-source BigFive personality traits test, 檢索日期：12月 19, 2025， [https://bigfive-test.com/](https://bigfive-test.com/)  
27. A Multiple Choice Quiz \- Using Streamlit, 檢索日期：12月 19, 2025， [https://discuss.streamlit.io/t/a-multiple-choice-quiz/55870](https://discuss.streamlit.io/t/a-multiple-choice-quiz/55870)  
28. Creating a basic quiz app \- Using Streamlit, 檢索日期：12月 19, 2025， [https://discuss.streamlit.io/t/creating-a-basic-quiz-app/2916](https://discuss.streamlit.io/t/creating-a-basic-quiz-app/2916)  
29. Radar chart (aka spider or star chart) — Matplotlib 3.10.8 documentation, 檢索日期：12月 19, 2025， [https://matplotlib.org/stable/gallery/specialty\_plots/radar\_chart.html](https://matplotlib.org/stable/gallery/specialty_plots/radar_chart.html)  
30. Step-by-Step Guide to Building an AI Voice Assistant with Streamlit & OpenAI \- YouTube, 檢索日期：12月 19, 2025， [https://www.youtube.com/watch?v=ZLiA\_pkRFsc](https://www.youtube.com/watch?v=ZLiA_pkRFsc)  
31. 專題報告格式說明.docx  
32. 檢索日期：1月 1, 1970， uploaded:image\_569451.jpg
