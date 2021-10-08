# core_nlp
[Core](https://core.ac.uk/) api로 수집한 논문 데이터에 NLP를 적용.  
이를 통해 현재 가지고 있는 reference paper와 유사한 paper 들을 clustering 한 문헌의 리스트를 연구자에게 제안 가능  

## 1. dielectric.ipynb
- core api v2 를 이용하여 논문을 수집  
- utils.py의 CoreApiRequestor 클래스에서 get_method_query_request_url 함수를 이용하여 파라미터로부터 쿼리를 완성시킬 때 params 의 설정에서 연도 설정이 불확실함  

## 2. utils.py  
- 문서 수집용 class  
- 그래프 출력을 위한 연도별 논문 발표 건수 데이터 만드는 year_profile 관련 함수  
- json format 으로 된 데이터를 pandas dataframe으로 변경  

## 3. nlp_utils.py  
- DocuVec : Document vector (paragraph vector) 를 embedding 하는 학습을 위한 함수  
- DocuSim : 생성된 모델에 새로운 데이터를 적용하는 함수  
- 개선 예정: 사용자 정의 stopword 추가  

## 4. papers  
- Reference 논문 데이터를 적용하여 현재 데이터 세트 내에서 비슷한 문헌을 찾을 때 이용할 txt 파일  

## 5. app.49978.pdf  
- 초기에는 pdf를 pypdf2 를 이용하여 text 추출하려고 했으나, 띄어쓰기 되어있지 않은 채 추출되어 임시로 txt 파일을 이용하게 되었음  
