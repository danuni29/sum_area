import os
import pandas as pd

# 특정 폴더에서 CSV 파일 가져오기
folder_path = './in'  # 폴더 경로 수정
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# 새로운 데이터프레임 생성
new_df = pd.DataFrame(columns=['ID', 'FAC_CODE'])

for file_name in csv_files:
    file_path = os.path.join(folder_path, file_name)

    # 오류 처리 코드 추가
    try:
        data = pd.read_csv(file_path, encoding='cp949')
    except pd.errors.ParserError:
        print(f"Error occurred while parsing the CSV file: {file_name}")
        continue  # 다음 파일로 넘어가기

    # 데이터 추출
    start_index = data.index[data.iloc[:, 0] == '[WATER_INSUPPLY:START]'][0] + 2
    end_index = data.index[data.iloc[:, 0] == '[WATER_INSUPPLY:END]'][0] - 1
    extracted_data = data.iloc[start_index:end_index, 1]

    # [PROJECT:START] 행 다음 데이터 추출
    project_start_index = data.index[data.iloc[:, 0] == '[PROJECT:START]'][0] + 1
    extracted_data2 = data.iloc[project_start_index:project_start_index + len(extracted_data), 0]

    # 데이터프레임으로 변환
    extracted_df = pd.DataFrame({'ID': extracted_data2, 'FAC_CODE': extracted_data})

    # 데이터프레임 확인
    print("Extracted DataFrame:")
    print(extracted_df)

    # 새로운 데이터프레임에 추가
    new_df = pd.concat([new_df, extracted_df], ignore_index=True)

# 결과를 엑셀 파일로 저장
output_file_path = 'out_2022.xlsx'
new_df.to_excel(output_file_path, index=False)
