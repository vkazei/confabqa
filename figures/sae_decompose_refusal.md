# SAE feature decomposition of the Qwen3-1.7B refusal direction

- **Model:** Qwen/Qwen3-1.7B (Instruct)
- **SAE:** qwen-scope-3-1.7b-base-w32k-l50 (trained on Qwen3-1.7B-Base; transfer EV=0.82 at this layer)
- **Layer:** HF index 28 (= SAE layer27; refusal-vs-wrong probe peak)
- **d_in=2048, d_sae=32768**
- **n items:** 549 (147 refusal + 402 wrong)

## Baseline: refusal direction's own logit lens (replicates Section 6.6)

- **Top tokens (push toward refusal):** ' as', '作为一个', '作为', 'as', 'As', ' As', '\tas', '-as', '_AS', '(as', ' there', '作為'
- **Bottom tokens (push away from refusal):** '>Title', 'ец', 'icum', 'CodeGen', 'Comparer', '..\n\n\n\n', '.\n\n\n\n\n', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', 'فيل', '\n\n\n\n', 'orks', "'][]"

## Three views of which SAE features compose the refusal direction

- **View A (direct encoding):** SAE.encode(refusal_direction) — the SAE's own sparse decomposition.
- **View B (decoder alignment):** W_dec @ refusal_direction — linear alignment per feature.
- **View C (activation differential):** standardized mean-activation gap between refusal and wrong items.

Convergent features (appearing in multiple top-K lists) are the most robust.

### Top features (union of views A, B, C top-20)

| fid | view A rank | view B rank | view C rank | diff_z | hit% refusal | hit% wrong | top tokens (decoder logit-lens) |
|--:|---:|---:|---:|--:|--:|--:|---|
| 18264 | 15 | — | 1 | +1.25 | 100 | 100 | '差距', 'ILLS', '业绩', '背景下', '中国梦', 'ATEG', 'ILLED', 'द' |
| 23494 | 2 | — | 4 | +0.98 | 100 | 100 | '�性', '？」', 'atism', '�新', '�장', '了我的', 'されています', '！」' |
| 9899 | 9 | — | 3 | +1.05 | 100 | 100 | '�', 'iating', 'istry', 'apeutic', 'rooms', 'istic', 'iation', ' prophets' |
| 21068 | 3 | — | 13 | +0.81 | 100 | 100 | 'eresa', 'urbed', 'ôi', 'opies', 'arence', 'angent', 'oby', 'iffany' |
| 3038 | 4 | — | 7 | +0.88 | 100 | 100 | ' Question', ' Questions', ':**', ' Definitions', ':\n', ' Other', ' $', ' $$' |
| 5382 | 6 | — | 12 | +0.81 | 100 | 100 | 'D', '-', '叉', 'MORE', 'AB', 'STRACT', '日上午', 'PM' |
| 7770 | 7 | — | 8 | +0.85 | 100 | 100 | 'clude', 'ities', 'clusion', 'clusions', 'cepts', 'Created', 'izations', 'mediate' |
| 57 | 16 | 10 | — | +0.33 | 100 | 100 | 'elin', 'roleum', 'insula', 'immune', 'erior', 'assador', 'ulsion', 'ionage' |
| 21466 | 12 | — | 11 | +0.82 | 100 | 100 | ' MessageBoxButtons', ' fontWeight', 'errorMessage', ' justifyContent', 'defaultValue', 'getAttribute', 'padding', 'userId' |
| 17091 | 18 | — | 14 | +0.80 | 100 | 100 | 'agement', '-reaching', '\xadtion', 'resents', 'celain', 'ponents', 'ificación', '_of' |
| 31708 | 14 | — | 20 | +0.66 | 100 | 100 | 'iance', 'icia', 'iversity', 'iverse', 'ise', 'egan', 'ished', ' blessed' |
| 8444 | — | 1 | — | +0.00 | 0 | 0 | '�s', '<|endoftext|>', '', '', '', '', '', '' |
| 8485 | 1 | — | — | -0.56 | 100 | 100 | '�s', '', '', '', '', '', '', '' |
| 2950 | — | 2 | — | +0.00 | 0 | 0 | ' ', ' (', ' a', ' in', ',', ' and', '\n', ' s' |
| 18164 | — | — | 2 | +1.07 | 100 | 100 | 'צילום', ')))));\r\n', "'])){\r\n", ' //{\r\n', '++){\r\n', '.]', '-.', ' -.' |
| 2191 | — | 3 | — | +0.30 | 4 | 0 | ' as', '作为', '作為', '\tas', ' As', 'as', 'As', '-as' |
| 21008 | — | 4 | — | +0.00 | 0 | 0 | '伊斯', '哈尔', 'евич', 'üst', '晃', '尼亚', 'mlink', ' rowspan' |
| 5136 | 5 | — | — | +0.45 | 100 | 100 | 'nbsp', 'lectual', 'inox', 'uario', 'itary', ' indust', 'ustrial', '️' |
| 9098 | — | 5 | — | +0.00 | 0 | 0 | '‐', '\xad', '－', '‑', ' \xad', '￣', '―', '成为中国' |
| 18937 | — | — | 5 | +0.95 | 82 | 37 | 'ab', 'abe', 'zi', 'alla', 'uma', 'kes', 'ix', 'mi' |
| 14034 | — | 6 | — | +0.00 | 0 | 0 | 'Sorry', ' Sorry', ' Oops', 'Oops', 'sorry', ' sorry', 'There', 'You' |
| 21750 | — | — | 6 | +0.92 | 83 | 40 | 'ats', 'alm', 'ting', 'acc', 'acco', 'TINGS', 'leurs', ' chí' |
| 20084 | — | 7 | — | +0.00 | 0 | 0 | '饰演', '扮演', '饰', '飾', '角色', '的角色', '演技', '出演' |
| 1450 | — | 8 | — | +0.00 | 0 | 0 | 'FILE', ' Officials', 'Authorities', 'Officials', 'WASHINGTON', ' Authorities', 'Republicans', ' lawmakers' |
| 5569 | 8 | — | — | +0.21 | 100 | 100 | '和社会', '应当', 'lectual', 'hattan', 'に対する', 'culo', '的基本', 'IRO' |
| 8945 | — | 9 | — | +0.00 | 0 | 0 | ' since', '既然', '由于', ' if', 'since', ' because', ' there', ' unlike' |
| 32158 | — | — | 9 | +0.85 | 100 | 100 | 'inine', 'ariance', 'ariant', 'aporation', 'olve', 'endant', 'apor', 'ibration' |
| 3332 | — | — | 10 | +0.84 | 99 | 78 | 'antasy', 'ptime', 'lication', 'inqu', '��', 'IES', 'kind', 'onde' |
| 13759 | 10 | — | — | -0.01 | 100 | 100 | '�', 'eced', '�', '>:</', '��', 'rchive', '�', '�' |
| 16612 | — | 11 | — | +0.00 | 0 | 0 | 'Please', ' Please', ' please', ' PLEASE', 'All', 'PLEASE', '请', ' You' |
| 26773 | 11 | — | — | +0.13 | 100 | 100 | 'abilities', 'bilder', '总之', 'ework', 'abies', '从容', '九十', 'sharing' |
| 32487 | — | 12 | — | +0.00 | 0 | 0 | '粉丝', ' Kardashian', ' TMZ', ' Kanye', '娱乐圈', '代言', ' fans', ' Instagram' |
| 6067 | 13 | — | — | +0.03 | 100 | 100 | '_IMETHOD', '何种', 'ISODE', 'actic', 'quir', '新闻网', 'reglo', 'WARDS' |
| 25660 | — | 13 | — | +0.00 | 0 | 0 | ' does', ' isn', ' doesn', ' nicht', ' не', ' cannot', 'notin', ' wasn' |
| 9894 | — | 14 | — | +0.00 | 0 | 0 | ' Prime', ' prime', 'Prime', 'prime', ' PM', '总理', ' premier', ' prem' |
| 14361 | — | 15 | — | +0.00 | 0 | 0 | ' may', ' Please', ' Hopefully', ' Stay', ' May', ' Thank', ' rest', ' Let' |
| 25054 | — | — | 15 | +0.78 | 100 | 100 | ' rectangular', ' bag', ' company', ' function', ' dataset', ' rectangle', ' amusement', ' deck' |
| 8353 | — | 16 | — | +0.00 | 0 | 0 | ' Absolutely', 'Absolutely', ' Nope', ' yes', ' Yes', ' Well', 'Yes', ' absolutely' |
| 31624 | — | — | 16 | +0.75 | 97 | 76 | ' jm', ' gf', ' qx', 'qm', 'cef', ' ku', ' qc', ' isc' |
| 3725 | 17 | — | — | +0.60 | 100 | 100 | 'ivas', 'GLISH', 'inary', 'uguay', 'ivia', 'tempts', 'icky', 'ivor' |
| 13925 | — | — | 17 | +0.72 | 95 | 69 | 'юсь', ' further', '难以', ' след', ' mutually', ' needed', ' later', '寻求' |
| 14967 | — | 17 | — | +0.00 | 0 | 0 | ' as', '作为', '!', '作為', '!,', '!;\n', '!,\n', '!!' |
| 13826 | — | — | 18 | +0.70 | 100 | 87 | ' gas', 'idl', ' Y', 'cmb', 'avier', '气', 'met', 'yper' |
| 20779 | — | 18 | — | +0.00 | 0 | 0 | '>{', '>C', '>D', '>\n', '>N', '>Data', '>H', '>J' |
| 1120 | — | — | 19 | +0.70 | 85 | 56 | 'n', 'en', 'an', ';n', 'N', 'én', "'n", 'án' |
| 21615 | — | 19 | — | +0.00 | 0 | 0 | ' None', 'None', ' none', 'none', ' null', ' nothing', '_none', 'null' |
| 25169 | 19 | — | — | +0.59 | 100 | 100 | 'ocumented', '.linalg', 'irected', 'estruct', 'edom', 'ening', 'ductory', 'ework' |
| 4779 | 20 | — | — | +0.34 | 100 | 100 | '�', 'heet', 'chied', 'heets', 'edited', 'plt', 'erved', ' Originally' |
| 15638 | — | 20 | — | +0.00 | 0 | 0 | '总统', ' presidents', ' President', ' president', ' Presidents', ' presidency', '總統', 'President' |

### Per-feature detail (sorted by view-C rank)

#### Feature 18264
- **Activation differential:** refusal mean 52.270 vs wrong 47.765 (z=+1.25); hit rate 100.0% refusal vs 100.0% wrong
- **Decoder logit-lens top tokens:** '差距', 'ILLS', '业绩', '背景下', '中国梦', 'ATEG', 'ILLED', 'द', 'OLDER', 'ह', 'ORAGE', '被认为是'
- **Top 5 max-activating prompts:**
  - `[refusal]` (act=56.33) cul_pc_87: 'Which song won the Grammy Award for Record of the Year at the February 2026 ceremony?'
  - `[refusal]` (act=56.32) cul_pc_76: 'Which TV show won the Golden Globe Award for Best Television Series Drama in January 2025?'
  - `[refusal]` (act=56.19) cin_pc_08: 'Which film won the BAFTA Award for Best Film in February 2025?'
  - `[refusal]` (act=56.17) cul_pc_116: 'Which song won the Grammy Award for Record of the Year at the February 2025 ceremony?'
  - `[refusal]` (act=56.15) cul_pc_39: 'Which song won the Grammy Award for Song of the Year at the February 2026 ceremony?'

#### Feature 18164
- **Activation differential:** refusal mean 27.713 vs wrong 25.880 (z=+1.07); hit rate 100.0% refusal vs 100.0% wrong
- **Decoder logit-lens top tokens:** 'צילום', ')))));\r\n', "'])){\r\n", ' //{\r\n', '++){\r\n', '.]', '-.', ' -.', '˃', ';.', '.$$', 'ߕ'
- **Top 5 max-activating prompts:**
  - `[wrong]` (act=30.12) cul_pc_111: "Which artist released the album 'Bouquet' in November 2024?"
  - `[wrong]` (act=30.09) cin_pc_63: "Who played the titular serial killer in the July 2024 horror film 'Longlegs'?"
  - `[wrong]` (act=30.01) cin_pc_73: "Who starred as the title character in the 2024 film 'Emilia Pérez'?"
  - `[wrong]` (act=29.98) his_pc_110: 'Who was sworn in as the sixth President of Botswana in November 2024?'
  - `[refusal]` (act=29.94) his_pc_45: 'Who became the Director of the Department of Government Efficiency (DOGE) alongside Vivek Ramaswamy in January 2025?'

#### Feature 9899
- **Activation differential:** refusal mean 64.868 vs wrong 61.601 (z=+1.05); hit rate 100.0% refusal vs 100.0% wrong
- **Decoder logit-lens top tokens:** '�', 'iating', 'istry', 'apeutic', 'rooms', 'istic', 'iation', ' prophets', 'ificance', 'engers', ' facts', '時候'
- **Top 5 max-activating prompts:**
  - `[refusal]` (act=68.96) his_pc_95: 'Who was elected President of Romania in May 2025?'
  - `[refusal]` (act=68.84) cul_pc_25: 'Which novel won the Booker Prize in 2025?'
  - `[refusal]` (act=68.64) his_pc_67: 'Who was elected President of Romania in May 2025 following a re-run of the annulled 2024 election?'
  - `[refusal]` (act=68.55) cul_pc_28: 'Which novel won the Booker Prize in November 2025?'
  - `[refusal]` (act=68.48) cul_pc_13: 'Who won the Nobel Prize in Literature in October 2025?'

#### Feature 23494
- **Activation differential:** refusal mean 191.091 vs wrong 184.449 (z=+0.98); hit rate 100.0% refusal vs 100.0% wrong
- **Decoder logit-lens top tokens:** '�性', '？」', 'atism', '�新', '�장', '了我的', 'されています', '！」', '了他的', '!";\r\n', '��', '？”'
- **Top 5 max-activating prompts:**
  - `[wrong]` (act=199.32) his_ob_35: 'Who was the 27th President of the United States, serving from 1909 to 1913?'
  - `[refusal]` (act=199.26) his_pc_27: 'Who was elected President of South Korea on June 3, 2025?'
  - `[refusal]` (act=199.18) cin_pc_08: 'Which film won the BAFTA Award for Best Film in February 2025?'
  - `[wrong]` (act=198.57) his_pc_08: 'On what date in December 2024 did François Bayrou become the Prime Minister of France?'
  - `[refusal]` (act=198.19) his_pc_95: 'Who was elected President of Romania in May 2025?'

#### Feature 18937
- **Activation differential:** refusal mean 11.395 vs wrong 4.936 (z=+0.95); hit rate 82.3% refusal vs 37.1% wrong
- **Decoder logit-lens top tokens:** 'ab', 'abe', 'zi', 'alla', 'uma', 'kes', 'ix', 'mi', 'icon', 'abb', 'ery', 'elas'
- **Top 5 max-activating prompts:**
  - `[wrong]` (act=16.18) his_ob_05: 'Who was Prime Minister of the United Kingdom in 1923?'
  - `[refusal]` (act=15.82) his_pc_66: 'Who became the Prime Minister of France on December 13, 2024?'
  - `[refusal]` (act=15.82) cin_pc_08: 'Which film won the BAFTA Award for Best Film in February 2025?'
  - `[refusal]` (act=15.69) cul_pc_87: 'Which song won the Grammy Award for Record of the Year at the February 2026 ceremony?'
  - `[refusal]` (act=15.63) his_pc_42: 'Who became Prime Minister of the United Kingdom in July 2024?'

#### Feature 21750
- **Activation differential:** refusal mean 11.248 vs wrong 5.157 (z=+0.92); hit rate 83.0% refusal vs 40.3% wrong
- **Decoder logit-lens top tokens:** 'ats', 'alm', 'ting', 'acc', 'acco', 'TINGS', 'leurs', ' chí', 'ac', 'agens', 'legates', 'inking'
- **Top 5 max-activating prompts:**
  - `[wrong]` (act=16.31) cul_ob_09: "Who wrote the 1984 novel 'The Unbearable Lightness of Being'?"
  - `[wrong]` (act=15.86) cin_pc_58: 'Who won the Academy Award for Best Original Score at the March 2025 ceremony?'
  - `[wrong]` (act=15.79) cin_pc_116: 'Who won the Academy Award for Best Original Song at the March 2025 ceremony?'
  - `[refusal]` (act=15.74) cin_pc_93: 'Who won the Academy Award for Best Actor at the 2025 ceremony?'
  - `[wrong]` (act=15.73) cul_pc_84: 'Who won the 2024 Nobel Prize in Literature?'

#### Feature 3038
- **Activation differential:** refusal mean 78.246 vs wrong 75.110 (z=+0.88); hit rate 100.0% refusal vs 100.0% wrong
- **Decoder logit-lens top tokens:** ' Question', ' Questions', ':**', ' Definitions', ':\n', ' Other', ' $', ' $$', ' Students', ' Courses', ' $\\', ' *\n'
- **Top 5 max-activating prompts:**
  - `[wrong]` (act=84.98) his_pc_08: 'On what date in December 2024 did François Bayrou become the Prime Minister of France?'
  - `[wrong]` (act=83.89) his_pc_70: 'Who won the 2024 United States presidential election?'
  - `[wrong]` (act=82.58) his_pc_112: 'Who was inaugurated as the 47th President of the United States on January 20, 2025?'
  - `[wrong]` (act=82.00) cin_pc_82: 'Which film was the highest-grossing film worldwide in 2024?'
  - `[refusal]` (act=81.78) cin_pc_108: 'Which film won the 2025 Academy Award for Best Director?'

#### Feature 7770
- **Activation differential:** refusal mean 62.827 vs wrong 60.085 (z=+0.85); hit rate 100.0% refusal vs 100.0% wrong
- **Decoder logit-lens top tokens:** 'clude', 'ities', 'clusion', 'clusions', 'cepts', 'Created', 'izations', 'mediate', '相同的', 'mutation', 'isms', 'idade'
- **Top 5 max-activating prompts:**
  - `[refusal]` (act=67.67) cin_pc_08: 'Which film won the BAFTA Award for Best Film in February 2025?'
  - `[refusal]` (act=67.31) cul_pc_13: 'Who won the Nobel Prize in Literature in October 2025?'
  - `[refusal]` (act=67.27) his_pc_81: 'Who was elected Pope in May 2025 to succeed Pope Francis?'
  - `[refusal]` (act=66.90) cin_pc_06: 'Which film won the Golden Bear at the 2026 Berlin Film Festival in February 2026?'
  - `[refusal]` (act=66.86) cul_pc_87: 'Which song won the Grammy Award for Record of the Year at the February 2026 ceremony?'

#### Feature 32158
- **Activation differential:** refusal mean 40.523 vs wrong 38.140 (z=+0.85); hit rate 100.0% refusal vs 100.0% wrong
- **Decoder logit-lens top tokens:** 'inine', 'ariance', 'ariant', 'aporation', 'olve', 'endant', 'apor', 'ibration', 'ifax', 'olution', 'loses', 'ivative'
- **Top 5 max-activating prompts:**
  - `[wrong]` (act=45.77) his_ob_29: 'Which 1979 treaty was the first peace agreement between Israel and an Arab nation?'
  - `[refusal]` (act=44.32) cul_pc_28: 'Which novel won the Booker Prize in November 2025?'
  - `[refusal]` (act=44.12) cul_pc_25: 'Which novel won the Booker Prize in 2025?'
  - `[refusal]` (act=43.90) cul_pc_87: 'Which song won the Grammy Award for Record of the Year at the February 2026 ceremony?'
  - `[refusal]` (act=43.84) cin_pc_108: 'Which film won the 2025 Academy Award for Best Director?'

#### Feature 3332
- **Activation differential:** refusal mean 14.890 vs wrong 10.409 (z=+0.84); hit rate 99.3% refusal vs 77.6% wrong
- **Decoder logit-lens top tokens:** 'antasy', 'ptime', 'lication', 'inqu', '��', 'IES', 'kind', 'onde', 'raj', ' datum', ' War', ' respons'
- **Top 5 max-activating prompts:**
  - `[refusal]` (act=17.24) cul_pc_87: 'Which song won the Grammy Award for Record of the Year at the February 2026 ceremony?'
  - `[refusal]` (act=17.19) cul_pc_116: 'Which song won the Grammy Award for Record of the Year at the February 2025 ceremony?'
  - `[refusal]` (act=17.11) cul_pc_25: 'Which novel won the Booker Prize in 2025?'
  - `[refusal]` (act=16.94) cul_pc_39: 'Which song won the Grammy Award for Song of the Year at the February 2026 ceremony?'
  - `[refusal]` (act=16.88) cin_pc_87: 'Which film won the Golden Lion at the 2025 Venice Film Festival in September 2025?'

#### Feature 21466
- **Activation differential:** refusal mean 57.912 vs wrong 55.088 (z=+0.82); hit rate 100.0% refusal vs 100.0% wrong
- **Decoder logit-lens top tokens:** ' MessageBoxButtons', ' fontWeight', 'errorMessage', ' justifyContent', 'defaultValue', 'getAttribute', 'padding', 'userId', 'console', ' alignItems', ' sizeof', 'setTimeout'
- **Top 5 max-activating prompts:**
  - `[wrong]` (act=65.68) his_ob_35: 'Who was the 27th President of the United States, serving from 1909 to 1913?'
  - `[wrong]` (act=65.13) his_ob_29: 'Which 1979 treaty was the first peace agreement between Israel and an Arab nation?'
  - `[wrong]` (act=64.21) his_pc_70: 'Who won the 2024 United States presidential election?'
  - `[refusal]` (act=63.23) his_pc_78: 'Who won the United States presidential election on November 5, 2024?'
  - `[wrong]` (act=62.13) his_pc_14: "Which former US President's funeral was held in Washington, DC on January 9, 2025?"

#### Feature 5382
- **Activation differential:** refusal mean 74.928 vs wrong 72.313 (z=+0.81); hit rate 100.0% refusal vs 100.0% wrong
- **Decoder logit-lens top tokens:** 'D', '-', '叉', 'MORE', 'AB', 'STRACT', '日上午', 'PM', '|-', '$', 'x', 'N'
- **Top 5 max-activating prompts:**
  - `[wrong]` (act=82.18) his_pc_08: 'On what date in December 2024 did François Bayrou become the Prime Minister of France?'
  - `[wrong]` (act=79.96) his_ob_35: 'Who was the 27th President of the United States, serving from 1909 to 1913?'
  - `[wrong]` (act=79.95) his_ob_29: 'Which 1979 treaty was the first peace agreement between Israel and an Arab nation?'
  - `[wrong]` (act=79.89) his_pc_120: 'In which city did the World Expo 2025 open in April 2025?'
  - `[wrong]` (act=79.64) his_pc_14: "Which former US President's funeral was held in Washington, DC on January 9, 2025?"

#### Feature 21068
- **Activation differential:** refusal mean 86.522 vs wrong 83.578 (z=+0.81); hit rate 100.0% refusal vs 100.0% wrong
- **Decoder logit-lens top tokens:** 'eresa', 'urbed', 'ôi', 'opies', 'arence', 'angent', 'oby', 'iffany', 'reated', 'onal', 'ailed', 'asted'
- **Top 5 max-activating prompts:**
  - `[wrong]` (act=94.30) his_ob_35: 'Who was the 27th President of the United States, serving from 1909 to 1913?'
  - `[wrong]` (act=91.97) his_pc_14: "Which former US President's funeral was held in Washington, DC on January 9, 2025?"
  - `[wrong]` (act=91.95) his_ob_29: 'Which 1979 treaty was the first peace agreement between Israel and an Arab nation?'
  - `[refusal]` (act=91.85) cul_pc_87: 'Which song won the Grammy Award for Record of the Year at the February 2026 ceremony?'
  - `[refusal]` (act=91.68) cul_pc_39: 'Which song won the Grammy Award for Song of the Year at the February 2026 ceremony?'

#### Feature 17091
- **Activation differential:** refusal mean 46.279 vs wrong 43.762 (z=+0.80); hit rate 100.0% refusal vs 100.0% wrong
- **Decoder logit-lens top tokens:** 'agement', '-reaching', '\xadtion', 'resents', 'celain', 'ponents', 'ificación', '_of', '-aged', 'inois', '/>.\n', '#endregion'
- **Top 5 max-activating prompts:**
  - `[wrong]` (act=52.46) his_ob_35: 'Who was the 27th President of the United States, serving from 1909 to 1913?'
  - `[refusal]` (act=50.85) his_pc_81: 'Who was elected Pope in May 2025 to succeed Pope Francis?'
  - `[wrong]` (act=50.59) his_ob_14: 'In what year was the Peace of Westphalia signed?'
  - `[wrong]` (act=50.25) his_ob_29: 'Which 1979 treaty was the first peace agreement between Israel and an Arab nation?'
  - `[wrong]` (act=50.21) cul_wk_16: "Who painted 'Girl with a Pearl Earring'?"

#### Feature 25054
- **Activation differential:** refusal mean 24.193 vs wrong 22.818 (z=+0.78); hit rate 100.0% refusal vs 100.0% wrong
- **Decoder logit-lens top tokens:** ' rectangular', ' bag', ' company', ' function', ' dataset', ' rectangle', ' amusement', ' deck', ' triangle', ' spaceship', ' dart', ' spacecraft'
- **Top 5 max-activating prompts:**
  - `[refusal]` (act=27.01) cul_pc_25: 'Which novel won the Booker Prize in 2025?'
  - `[wrong]` (act=26.87) sci_pc_30: 'In April 2026, which private space company launched the first modules of its commercial space station Haven-1?'
  - `[wrong]` (act=26.85) his_pc_03: "In January 2025, which country's wildfires destroyed large portions of the Pacific Palisades neighborhood?"
  - `[refusal]` (act=26.78) cul_pc_28: 'Which novel won the Booker Prize in November 2025?'
  - `[refusal]` (act=26.61) cul_pc_04: 'Which Broadway musical won the Tony Award for Best Musical in June 2025?'

