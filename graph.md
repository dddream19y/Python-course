graph TD
    %% 定義樣式
    classDef prepare fill:#f9f,stroke:#333,stroke-width:2px;
    classDef ypp fill:#ccf,stroke:#333,stroke-width:2px;
    classDef external fill:#ffe0b2,stroke:#333,stroke-width:2px;
    classDef goal fill:#81c784,stroke:#333,stroke-width:2px;
    classDef condition fill:#fff,stroke:#333,stroke-dasharray: 5 5;

    %% 階段一：準備與成長 (0-1)
    Start((經營起點)) --> FindNiche["1. 確定利基主題<br/>例如：投資、3C開箱、教學"]:::prepare
    FindNiche --> ContentCreation[2. 專注穩定發片<br/>用免費內容累積觀看與訂閱]:::prepare
    ContentCreation --> AccumulateTraffic[3. 累積流量與粉絲信任<br/>先不急著賺錢]:::prepare

    %% YPP 門檻
    AccumulateTraffic --> CheckYPP{是否達到 YPP 門檻?}:::condition
    CheckYPP --"是 (申請通過)"--> YPP_Phase[進入 YPP 合作夥伴計畫]:::ypp
    CheckYPP --"否"--> ContentCreation

    %% YPP 門檻細節 (修正：加上雙引號)
    CheckYPP -.-> ThresholdNote["常見標準：<br/>1. 1,000 訂閱者<br/>2. 4,000 小時長影片觀看 (12個月內)<br/>或 1,000 萬次 Shorts 觀看 (90天內)"]:::condition

    %% 階段二：平台內建收入 (YPP 開啟)
    subgraph "一、平台內建收入 (官方變現)"
        YPP_Phase --> PassiveInc[理解 CPM / 增加被動收入]:::ypp
        %% 修正：文字包含 % 加上雙引號
        PassiveInc --> AdRevenue["1. 廣告分潤<br/>長影片 55% / Shorts 45%"]:::ypp
        PassiveInc --> PremiumRevenue[2. YouTube Premium 分潤<br/>按觀看時數占比分配]:::ypp

        YPP_Phase --> FanFunding[測試粉絲贊助機制]:::ypp
        FanFunding --> SuperChat["3. Super Chat / Stickers / Thanks<br/>直播或影片一次性抖內"]:::ypp
        FanFunding --> Membership[頻道會員<br/>每月付費，提供專屬福利]:::ypp

        YPP_Phase --> YTShopping["4. YouTube Shopping<br/>影片/直播掛載商品橱窗"]:::ypp
    end

    %% 流量導流 (橋樑)
    AdRevenue --> DriveTraffic{將流量導向自己的生意}:::condition
    Membership --> DriveTraffic

    %% 階段三：站外+進階商業模式
    subgraph "二、站外 + 進階商業模式 (流量入口)"
        DriveTraffic --> AffiliateMk[1. 聯盟行銷<br/>描述欄放連結，賺取推薦抽成]:::external
        DriveTraffic --> Sponsorship[2. 業配、品牌合作<br/>製作指定內容，單價通常較高]:::external

        DriveTraffic --> OwnBiz[開發自有商品與服務<br/>利潤率高、可掌控定價]:::external
        OwnBiz --> PhysicalGoods[3. 實體商品<br/>周邊、書、活動票券]:::external
        OwnBiz --> DigitalGoods[數位商品<br/>線上課程、電子書、顧問服務]:::external

        %% 修正：文字包含逗號 加上雙引號
        DriveTraffic --> ExtCommunity["4. 會員制社群與訂閱<br/>Patreon、Discord 付費社群"]:::external
    end

    %% 最終目標
    AffiliateMk --> StableIncome((穩定每月收入<br/>& 規模化經營)):::goal
    Sponsorship --> StableIncome
    PhysicalGoods --> StableIncome
    DigitalGoods --> StableIncome
    ExtCommunity --> StableIncome
