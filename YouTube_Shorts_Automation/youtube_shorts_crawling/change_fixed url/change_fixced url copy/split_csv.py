import os
import pandas as pd

def split_excel(input_file, output_folder, max_records):
    try:
        # 엑셀 파일을 읽음
        df = pd.read_excel(input_file)

        # 총 행 수 계산
        total_rows = len(df)
        file_index = 1

        # 출력 폴더 생성
        os.makedirs(output_folder, exist_ok=True)

        for start_row in range(0, total_rows, max_records):
            end_row = min(start_row + max_records, total_rows)
            split_df = df.iloc[start_row:end_row]

            # 출력 파일 경로 설정
            output_file = os.path.join(output_folder, f'split_{file_index}.xlsx')

            # 분할된 데이터를 새로운 엑셀 파일로 저장
            split_df.to_excel(output_file, index=False, engine='openpyxl')

            print(f'파일 {output_file} 생성 완료 ({start_row + 1}에서 {end_row}행까지)')

            file_index += 1

        print("엑셀 파일이 성공적으로 분할되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

# Example usage:
input_file = "C:/Users/T14Gen1/Documents/카카오톡 받은 파일/change_fixced url copy/Youtube_Data_2024-05-14.xlsx"
output_folder = 'C:/Users/T14Gen1/Documents/카카오톡 받은 파일/change_fixced url copy/'  # 폴더 경로
split_excel(input_file, output_folder, max_records=300)
