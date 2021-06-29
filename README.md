# core_nlp
core api로 수집한 논문의 자연어처리

## 1. dielectric.ipynb
- core api v2 를 이용하여 논문을 수집
- utils.py의 CoreApiRequestor 클래스에서 get_method_query_request_url 함수를 이용하여 파라미터로부터 쿼리를 완성시킬 때 params 의 설정에서 연도 설정이 불확실함

## 2. utils.py
- 문서 수집용 class
- 그래프 출력을 위한 연도별 논문 발표 건수 데이터 만드는 year_profile 관련 함수
- json format 으로 된 데이터를 pandas dataframe으로 변경

## 3. nlp_utils.py
- 개선 필요 : 함수 안에서 stopword를 따로따로 설정하는 것이 현재 문제 (stopword 추가 시 대응이 되지 않음)
- DocuVec : Document vector (paragraph vector) 를 embedding 하는 학습을 위한 함수
- DocuSim : 생성된 모델에 새로운 데이터를 적용하는 함수

## 4. papers
- reference 논문 데이터를 적용하여 현재 데이터 세트 내에서 비슷한 문헌을 찾을 때 이용할 txt 파일

## 5. app.49978.pdf
- 초기에는 pdf를 pypdf2 를 이용하여 text 추출하려고 했으나, 띄어쓰기 되어있지 않은 채 추출되어 임시로 txt 파일을 이용하게 되었음
