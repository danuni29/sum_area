import os
import pandas as pd
import csv

def main():
    # 파일 읽기
    folder_path = './in'
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    new_df = pd.DataFrame(columns=['ID', 'AREA'])

    for file_name in csv_files:
        file_path = os.path.join(folder_path, file_name)

        # data = pd.read_csv(file_path, encoding='cp949')
        # 오류 처리 코드 추가
        # pandas.errors.ParserError: Errortokenizing data.
        try:
            data = pd.read_csv(file_path, encoding='cp949')

        except pd.errors.ParserError:
            print(f"Error occurred while parsing the CSV file: {file_name}")
            f = open(file_path, encoding='cp949')
            reader = csv.reader(f)
            csv_list = []
            for i in reader:
                csv_list.append(i)
            f.close()
            data = pd.DataFrame(csv_list)

            # continue  # 다음 파일로 넘어가기

        # ID추출
        project_start_index = data.index[data.iloc[:, 0] == '[PROJECT:START]'][0] + 1
        extracted_ID = data.iloc[project_start_index, 0]

        print(extracted_ID)

        # 면적 합 계산
        benefit_area_start_index = data.index[data.iloc[:, 0] == '[BENEFITAREA:START]'][0] + 4
        benefit_area_end_index = data.index[data.iloc[:, 0] == '[BENEFITAREA:END]'][0]

        sum_extracted_area = data.iloc[benefit_area_start_index:benefit_area_end_index, 4].astype(float).sum()
        extracted_area = data.iloc[benefit_area_start_index:benefit_area_end_index, 4].astype(float)
        print(extracted_area)


        # 새로운 데이터프레임에 추가
        # extracted_df = pd.DataFrame({'ID': extracted_ID, 'AREA': sum_extracted_area})
        extracted_df = pd.DataFrame({'ID': [extracted_ID], 'AREA': [sum_extracted_area]})
        new_df = pd.concat([new_df, extracted_df], ignore_index=True)
        print(f"new_df:{new_df}")


    # 결과를 엑셀 파일로 저장
    output_file_path = 'output.xlsx'
    new_df.to_excel(output_file_path, index=False)

if __name__ == '__main__':
    main()