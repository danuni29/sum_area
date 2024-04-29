import os
import io
from typing import List

import pandas as pd


def find_idx_start_with(full_text: List[str], query: str):
    for i, line in enumerate(full_text):
        if line.startswith(query):
            return i
    return None


def main():
    # 특정 폴더에서 CSV 파일 가져오기
    folder_path = r'C:\Users\Shin\Desktop\2022\test'  # 폴더 경로 수정
    folder_path = r'./in'  # 폴더 경로 수정해서 쓰세요.
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    dataset = []

    for file_name in csv_files:
        file_path = os.path.join(folder_path, file_name)

        # CSV 파일 읽기
        with open(file_path, encoding="cp949") as f:
            full_text = [x.strip() for x in f.readlines()]
            prj_idx_s = find_idx_start_with(full_text, "[PROJECT:START]")
            prj_idx_e = find_idx_start_with(full_text, "[PROJECT:END]")
            if prj_idx_e - prj_idx_s != 2:
                print(f"{file_path}의 [PROJECT:START] 행을 확인하세요. line={prj_idx_s + 1}")
                continue
            project_name = full_text[prj_idx_s + 1].split(",")[0]

            benefit_area_idx_s = find_idx_start_with(full_text, "[BENEFITAREA:START]")
            benefit_area_idx_e = find_idx_start_with(full_text, "[BENEFITAREA:END]")
            benefit_area_count = int(full_text[benefit_area_idx_s + 2].split(",")[1])
            if benefit_area_idx_e - benefit_area_idx_s != benefit_area_count + 4:
                print(f"{file_path}의 [BENEFITAREA:START] 행을 확인하세요. line={benefit_area_idx_s + 1}")

            benefit_area_txt = io.StringIO("\n".join(full_text[benefit_area_idx_s + 3:benefit_area_idx_e]))

            df = pd.read_csv(benefit_area_txt)
            # print(df.head())
            # print(df.tail())
            # print(df["면적(㎡)"].sum())

            data = {'ID': project_name,
                    'AREA': df["면적(㎡)"].sum()}

            dataset.append(data)

    df_output = pd.DataFrame(dataset)
    # # 결과를 엑셀 파일로 저장
    output_file_path = 'out_2022.xlsx'
    df_output.to_excel(output_file_path, index=False)


if __name__ == "__main__":
    main()