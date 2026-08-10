# SAST Report — juice-shop-juice-shop

- **repo url**: `https://github.com/juice-shop/juice-shop.git`
- **branch**: `master`
- **commit**: `a520e158cb65c43d24e2c55d84f09b05a2511a03`
- **job id**: `local-1786284566`
- **project**: `juice-shop-juice-shop`
- **scanned at**: `2026-08-09T14:13:35+00:00`
- **duration sec**: `248.3`
- **sonar host**: `http://sonarqube:9000`

## Severity summary

| Severity | Count |
|---|---:|
| critical | 1 |
| high | 3705 |
| medium | 760 |
| low | 373 |
| info | 48 |

**Total: 4887**

## Findings

| Sev | Rule | Location | Message |
|---|---|---|---|
| critical | `secrets:S6706` | `lib/insecurity.ts:21` | Make sure this private key gets revoked, changed, and removed from the code. |
| high | `typescript:S6861` | `data/datacache.ts:33` | Exporting mutable 'let' binding, use 'const' instead. |
| high | `typescript:S3776` | `data/datacreator.ts:68` | Refactor this function to reduce its Cognitive Complexity from 55 to the 15 allowed. |
| high | `typescript:S2004` | `data/datacreator.ts:463` | Refactor this code to not nest functions more than 4 levels deep. |
| high | `typescript:S3504` | `data/static/codefixes/adminSectionChallenge_3.ts:3` | Unexpected var, use let or const instead. |
| high | `typescript:S3504` | `data/static/codefixes/adminSectionChallenge_3.ts:3` | Unexpected var, use let or const instead. |
| high | `typescript:S3776` | `frontend/src/app/Services/chat.service.ts:42` | Refactor this function to reduce its Cognitive Complexity from 31 to the 15 allowed. |
| high | `typescript:S3776` | `frontend/src/app/about/about.component.ts:74` | Refactor this function to reduce its Cognitive Complexity from 17 to the 15 allowed. |
| high | `typescript:S3735` | `frontend/src/app/challenge-solved-notification/challenge-solved-notification.component.ts:167` | Remove this use of the "void" operator. |
| high | `typescript:S1186` | `frontend/src/app/chatbot/chat-conversation/chat-conversation.component.spec.ts:105` | Unexpected empty async generator function 'emptyStream'. |
| high | `typescript:S1186` | `frontend/src/app/chatbot/chat-conversation/chat-conversation.component.spec.ts:115` | Unexpected empty async generator function 'emptyStream'. |
| high | `typescript:S1186` | `frontend/src/app/chatbot/chat-conversation/chat-conversation.component.spec.ts:124` | Unexpected empty async generator function 'emptyStream'. |
| high | `typescript:S1186` | `frontend/src/app/chatbot/chat-conversation/chat-conversation.component.spec.ts:134` | Unexpected empty async generator function 'emptyStream'. |
| high | `typescript:S1186` | `frontend/src/app/chatbot/chat-conversation/chat-conversation.component.spec.ts:169` | Unexpected empty async generator function 'emptyStream'. |
| high | `typescript:S1186` | `frontend/src/app/chatbot/chat-conversation/chat-conversation.component.spec.ts:193` | Unexpected empty async generator function 'emptyStream'. |
| high | `typescript:S3735` | `frontend/src/app/chatbot/chat-conversation/chat-conversation.component.ts:79` | Remove this use of the "void" operator. |
| high | `typescript:S3735` | `frontend/src/app/chatbot/chat-welcome-page/chat-welcome-page.component.ts:25` | Remove this use of the "void" operator. |
| high | `typescript:S3735` | `frontend/src/app/chatbot/chat-welcome-page/chat-welcome-page.component.ts:29` | Remove this use of the "void" operator. |
| high | `typescript:S2871` | `frontend/src/app/coding-challenge-page/components/coding-challenge-fix-it/coding-challenge-fix-it.component.spec.ts:172` | Provide a compare function to avoid sorting elements alphabetically. |
| high | `typescript:S2004` | `frontend/src/app/product/product.component.ts:90` | Refactor this code to not nest functions more than 4 levels deep. |
| high | `typescript:S2004` | `frontend/src/app/product/product.component.ts:112` | Refactor this code to not nest functions more than 4 levels deep. |
| high | `typescript:S2004` | `frontend/src/app/product/product.component.ts:147` | Refactor this code to not nest functions more than 4 levels deep. |
| high | `typescript:S2004` | `frontend/src/app/product/product.component.ts:154` | Refactor this code to not nest functions more than 4 levels deep. |
| high | `typescript:S7059` | `frontend/src/app/score-board/components/challenge-card/challenge-card.component.ts:37` | Refactor this asynchronous operation outside of the constructor. |
| high | `typescript:S1186` | `frontend/src/app/search-result/search-result.component.spec.ts:31` | Unexpected empty method 'observe'. |
| high | `typescript:S1186` | `frontend/src/app/search-result/search-result.component.spec.ts:32` | Unexpected empty method 'unobserve'. |
| high | `typescript:S1186` | `frontend/src/app/search-result/search-result.component.spec.ts:33` | Unexpected empty method 'disconnect'. |
| high | `typescript:S1186` | `frontend/src/app/search-result/search-result.component.spec.ts:310` | Unexpected empty method 'unobserve'. |
| high | `typescript:S1186` | `frontend/src/app/search-result/search-result.component.spec.ts:311` | Unexpected empty method 'disconnect'. |
| high | `typescript:S2004` | `frontend/src/app/server-started-notification/server-started-notification.component.ts:46` | Refactor this code to not nest functions more than 4 levels deep. |
| high | `typescript:S2004` | `frontend/src/app/server-started-notification/server-started-notification.component.ts:49` | Refactor this code to not nest functions more than 4 levels deep. |
| high | `typescript:S2004` | `frontend/src/app/server-started-notification/server-started-notification.component.ts:57` | Refactor this code to not nest functions more than 4 levels deep. |
| high | `typescript:S2004` | `frontend/src/app/server-started-notification/server-started-notification.component.ts:60` | Refactor this code to not nest functions more than 4 levels deep. |
| high | `typescript:S3776` | `frontend/src/app/web3-sandbox/web3-sandbox.component.ts:211` | Refactor this function to reduce its Cognitive Complexity from 16 to the 15 allowed. |
| high | `javascript:S3504` | `frontend/src/assets/private/EffectComposer.js:11` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/EffectComposer.js:12` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/EffectComposer.js:13` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/EffectComposer.js:38` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/EffectComposer.js:61` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/EffectComposer.js:63` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/EffectComposer.js:77` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/EffectComposer.js:126` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/MaskPass.js:22` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/MaskPass.js:31` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/MaskPass.js:80` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:73` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:75` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:77` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:78` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:79` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:81` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:82` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:83` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:85` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:86` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:87` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:89` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:90` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:91` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:92` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:94` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:96` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:97` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:101` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:131` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:132` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:144` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:145` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:157` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:162` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:163` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:164` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:213` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:214` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:218` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:222` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:239` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:323` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:392` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:424` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:474` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:475` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:476` | Unexpected var, use let or const instead. |
| high | `javascript:S3776` | `frontend/src/assets/private/OrbitControls.js:494` | Refactor this function to reduce its Cognitive Complexity from 18 to the 15 allowed. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:501` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:524` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:525` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/OrbitControls.js:526` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:7` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:27` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:28` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:30` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:41` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:42` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:280` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:291` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:292` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:310` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:324` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:338` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:350` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:403` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:439` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:441` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:443` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:444` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:446` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:447` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:456` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:488` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:724` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:725` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:726` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:727` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:728` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:729` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:787` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:806` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:865` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:867` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:942` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:985` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:986` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1008` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1012` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1040` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1041` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1054` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1283` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1364` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1458` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1465` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1708` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1730` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1746` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1747` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1748` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1750` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1764` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1766` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1780` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1782` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1783` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1795` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1796` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1797` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1799` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1800` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1801` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1802` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1806` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1807` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1808` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1809` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1826` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1828` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1854` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:1960` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2058` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2088` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2100` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2101` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2113` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2131` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2150` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2164` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2180` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2181` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2182` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2235` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2236` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2237` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2248` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2250` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2474` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2475` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2476` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2477` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2479` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2494` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2522` | Unexpected var, use let or const instead. |
| high | `javascript:S3776` | `frontend/src/assets/private/three.js:2542` | Refactor this function to reduce its Cognitive Complexity from 23 to the 15 allowed. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2548` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2583` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2584` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2585` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2586` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2587` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2588` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2648` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2776` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:2878` | Unexpected var, use let or const instead. |
| high | `javascript:S3776` | `frontend/src/assets/private/three.js:3035` | Refactor this function to reduce its Cognitive Complexity from 25 to the 15 allowed. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3037` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3041` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3042` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3043` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3044` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3160` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3166` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3167` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3168` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3169` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3227` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3317` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3324` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3343` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3351` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3352` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3359` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3360` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3362` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3378` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3380` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3437` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3442` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3480` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3484` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3522` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3529` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3589` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3615` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3622` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3626` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3739` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3744` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3762` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3766` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3782` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3786` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3796` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3798` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3846` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3853` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3918` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3946` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3953` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3957` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3966` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:3970` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4001` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4066` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4080` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4106` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4136` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4143` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4165` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4177` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4179` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4192` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4193` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4205` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4211` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4237` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4249` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4279` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4305` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4317` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4352` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4367` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4410` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4411` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4423` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4427` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4428` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4430` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4431` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4432` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4460` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4462` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4463` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4464` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4465` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4469` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4485` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4501` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4517` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4533` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4549` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4590` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4592` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4593` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4594` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4595` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4596` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4627` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4628` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4629` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4633` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4680` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4681` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4682` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4684` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4685` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4686` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4687` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4689` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4690` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4691` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4692` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4720` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4735` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4769` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4776` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4813` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4815` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4816` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4817` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4818` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4863` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4864` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4880` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4908` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4914` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4923` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4936` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4937` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4939` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4940` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4941` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4942` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4961` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:4965` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5020` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5021` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5034` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5036` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5037` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5038` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5061` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5078` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5095` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5114` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5115` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5116` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5117` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5118` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5160` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5161` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5165` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5167` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5168` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5169` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5172` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5185` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5186` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5187` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5215` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5216` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5217` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5219` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5220` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5221` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5222` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5235` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5236` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5237` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5238` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5246` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5247` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5248` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5249` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5251` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5252` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5253` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5274` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5287` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5337` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5345` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5359` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5361` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5375` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5379` | Unexpected var, use let or const instead. |
| high | `javascript:S3776` | `frontend/src/assets/private/three.js:5397` | Refactor this function to reduce its Cognitive Complexity from 31 to the 15 allowed. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5406` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5407` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5408` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5409` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5410` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5411` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5412` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5413` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5414` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5415` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5434` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5525` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5533` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5549` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5565` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5575` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5588` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5602` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5604` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5608` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5669` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5670` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5671` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5672` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5687` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5688` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5707` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5716` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5733` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5800` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5804` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5816` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5818` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5861` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5869` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5871` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5887` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5954` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5969` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5971` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5983` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5984` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5985` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5986` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5987` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:5988` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6003` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6007` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6022` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6023` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6024` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6026` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6028` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6044` | Unexpected var, use let or const instead. |
| high | `javascript:S3776` | `frontend/src/assets/private/three.js:6047` | Refactor this function to reduce its Cognitive Complexity from 16 to the 15 allowed. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6049` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6051` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6053` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6062` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6063` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6082` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6084` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6150` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6151` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6155` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6181` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6218` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6220` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6229` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6230` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6238` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6242` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6244` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6246` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6262` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6279` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6286` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6287` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6288` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6294` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6295` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6297` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6341` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6342` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6343` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6347` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6462` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6474` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6504` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6512` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6549` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6567` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6617` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6660` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6684` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6688` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6694` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6711` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6712` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6713` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6721` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6722` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6723` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6724` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6725` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6727` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6729` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6738` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6739` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6740` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6751` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6755` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6799` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6800` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6815` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6828` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6917` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6927` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6967` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:6987` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:7003` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:7004` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:7008` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:7024` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:7025` | Unexpected var, use let or const instead. |
| high | `javascript:S3504` | `frontend/src/assets/private/three.js:7031` | Unexpected var, use let or const instead. |