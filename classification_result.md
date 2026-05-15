프롬프트1:
PROMPT_TEMPLATE = """
You are an expert Web Application Firewall (WAF) analyst.

Your task is to classify the following HTTP request as either:
- "Normal"
- "Anomalous"

Analyze the request carefully using common web attack indicators including:
- SQL Injection (SQLi)
- Cross-Site Scripting (XSS)
- Command Injection
- Path Traversal
- Remote Code Execution (RCE)
- File Inclusion
- Suspicious encoding or obfuscation
- Abnormal headers or payloads
- Scanner/probing behavior

A request is "Normal" if it appears to be legitimate browser or API traffic without malicious intent.

A request is "Anomalous" if it contains attack patterns, malicious payloads, exploitation attempts, suspicious encoding, or behavior inconsistent with normal web usage.

Rules:
- Consider URL decoding and common obfuscation techniques.
- Focus on intent, not only syntax.
- Be conservative but accurate.
- Output ONLY valid JSON.

Examples:

Request:
GET /index.jsp HTTP/1.1

Output:
{{"label": "Normal", "reason": "Legitimate request for a web page with no suspicious indicators"}}

Request:
GET /search?q=' OR '1'='1 HTTP/1.1

Output:
{{"label": "Anomalous", "reason": "SQL injection attempt using authentication bypass pattern"}}

Now analyze this request:

Request:
{http_text}

Output:
"""

결과:10/100건 완료 (10.5초, 건당 1.05초)
  20/100건 완료 (20.5초, 건당 1.02초)
  30/100건 완료 (32.0초, 건당 1.07초)
  40/100건 완료 (43.4초, 건당 1.09초)
  50/100건 완료 (56.0초, 건당 1.12초)
  60/100건 완료 (68.2초, 건당 1.14초)
  70/100건 완료 (78.7초, 건당 1.12초)
  80/100건 완료 (89.2초, 건당 1.11초)
  90/100건 완료 (99.2초, 건당 1.10초)
  100/100건 완료 (109.7초, 건당 1.10초)

총 소요: 109.7초
1만 건 환산: 약 183분

LLM 정확도: 0.4600
LLM F1:    0.6143
분류 실패(Unknown): 0건

              precision    recall  f1-score   support

      Normal       0.75      0.05      0.10        56
   Anomalous       0.45      0.98      0.61        44

    accuracy                           0.46       100
   macro avg       0.60      0.52      0.36       100
weighted avg       0.62      0.46      0.33       100


프롬프트2:PROMPT_TEMPLATE = """
You are a senior cybersecurity analyst specializing in HTTP threat detection.

Determine whether the following HTTP request is:
1. Normal
2. Anomalous

Use the following methodology:
1. Identify suspicious keywords, operators, payloads, encodings, or abnormal structures.
2. Determine whether the request resembles known attack techniques.
3. Evaluate whether the request behavior matches legitimate web traffic.
4. Produce a concise security explanation.

Known attack categories include:
- SQL Injection
- XSS
- Path Traversal
- Command Injection
- SSTI
- RCE
- File Inclusion
- Credential attacks
- Reconnaissance/scanning
- Malicious automation

Important:
- Attack payloads may be URL-encoded or obfuscated.
- Do not classify a request as anomalous solely because it contains special characters.
- Consider the full context of the request.

Return ONLY this JSON format:
{{"label":"Normal|Anomalous","reason":"short explanation"}}

HTTP Request:
{http_text}
"""

결과:10/100건 완료 (10.2초, 건당 1.02초)
  20/100건 완료 (20.7초, 건당 1.04초)
  30/100건 완료 (31.7초, 건당 1.06초)
  40/100건 완료 (42.5초, 건당 1.06초)
  50/100건 완료 (54.1초, 건당 1.08초)
  60/100건 완료 (65.3초, 건당 1.09초)
  70/100건 완료 (75.9초, 건당 1.08초)
  80/100건 완료 (86.5초, 건당 1.08초)
  90/100건 완료 (96.5초, 건당 1.07초)
  100/100건 완료 (107.5초, 건당 1.07초)

총 소요: 107.5초
1만 건 환산: 약 179분

LLM 정확도: 0.5200
LLM F1:    0.6129
분류 실패(Unknown): 1건

              precision    recall  f1-score   support

      Normal       0.70      0.25      0.37        56
   Anomalous       0.47      0.86      0.61        44

    accuracy                           0.52       100
   macro avg       0.59      0.56      0.49       100
weighted avg       0.60      0.52      0.48       100

프롬프트3:
PROMPT_TEMPLATE = """
당신은 HTTP 웹 공격 탐지 전문가입니다.

아래 HTTP 요청을 분석하여 다음 두 가지 중 하나로 분류하세요:
- "Normal"
- "Anomalous"

다음 기준을 기반으로 요청을 분석하세요:
1. 의심스러운 키워드, 연산자, 페이로드, 인코딩 여부 확인
2. 알려진 웹 공격 패턴과 유사한지 판단
3. 정상적인 웹 트래픽인지 평가
4. 짧고 명확한 보안 분석 이유 작성

탐지 대상 공격 유형:
- SQL Injection(SQLi)
- Cross Site Scripting(XSS)
- Path Traversal
- Command Injection
- SSTI
- Remote Code Execution(RCE)
- File Inclusion
- 인증 우회 공격
- 스캐닝 및 정찰 행위
- 자동화된 악성 요청

중요 규칙:
- URL 인코딩 및 난독화(obfuscation)를 고려하세요.
- 특수문자가 있다고 해서 무조건 공격으로 판단하지 마세요.
- 요청 전체 문맥을 기반으로 판단하세요.
- 실제 공격 의도가 있는지 분석하세요.
- 반드시 JSON만 출력하세요.
- 추가 설명이나 markdown 없이 출력하세요.

출력 형식:
{{"label":"Normal|Anomalous","reason":"짧은 설명"}}

예시:

Request:
GET /index.jsp HTTP/1.1

Output:
{{"label":"Normal","reason":"정상적인 웹 페이지 요청"}}

Request:
GET /search?q=' OR '1'='1 HTTP/1.1

Output:
{{"label":"Anomalous","reason":"SQL Injection 인증 우회 패턴 탐지"}}

Request:
GET /?file=../../etc/passwd HTTP/1.1

Output:
{{"label":"Anomalous","reason":"Path Traversal 공격 시도"}}

이제 아래 요청을 분석하세요.

HTTP Request:
{http_text}

Output:
"""

결과:10/100건 완료 (7.1초, 건당 0.71초)
  20/100건 완료 (13.1초, 건당 0.66초)
  30/100건 완료 (19.4초, 건당 0.65초)
  40/100건 완료 (26.2초, 건당 0.65초)
  50/100건 완료 (34.1초, 건당 0.68초)
  60/100건 완료 (41.3초, 건당 0.69초)
  70/100건 완료 (47.5초, 건당 0.68초)
  80/100건 완료 (54.1초, 건당 0.68초)
  90/100건 완료 (60.6초, 건당 0.67초)
  100/100건 완료 (66.8초, 건당 0.67초)

총 소요: 66.8초
1만 건 환산: 약 111분

LLM 정확도: 0.5900
LLM F1:    0.6435
분류 실패(Unknown): 0건

              precision    recall  f1-score   support

      Normal       0.76      0.39      0.52        56
   Anomalous       0.52      0.84      0.64        44

    accuracy                           0.59       100
   macro avg       0.64      0.62      0.58       100
weighted avg       0.65      0.59      0.57       100