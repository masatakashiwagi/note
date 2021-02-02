import os
import argparse
import pandas as pd
import numpy as np

from logger import get_logger


LOGGER = get_logger()


def get_args():
    """Get arguments method."""
    parser = argparse.ArgumentParser(description="import input file.")
    parser.add_argument(
        "-i",
        "--input_file_path",
        required=True,
        type=str,
        help="input file path.",
    )

    return parser.parse_args()


def preprocess(path: str) -> None:
	"""Preprocess for dataframe."""
	# データセットのロード
	LOGGER.info("Load dataset.")
	df = pd.read_csv(path, skiprows=1, header=0)

	# 0行目は単位なので、削除する
	LOGGER.info("Delete 0 rows for unit.")
	df.drop(0, inplace=True)

	# NaNを0で埋める
	LOGGER.info("Fill NaN with 0.")
	df = df.fillna(0)
	
	# 日付をdatetime型に変換する
	LOGGER.info("Convert date to datetime type.")
	df["日付"] = pd.to_datetime(df["日付"])

	# 不要なカラムを削除する
	LOGGER.info("Delete unnecessary columns.")
	drop_cols = []
	for col in df.columns.tolist():
	    if col[-1] == '1':
	        drop_cols.append(col)
	df.drop(drop_cols, axis=1, inplace=True)

	# ファイルを保存する
	LOGGER.info("Save output file.")
	output_file = os.path.splitext(path)[0] + "_preprocess.csv"
	df.to_csv(output_file, index=False)



def main():
	"""Main function."""
	arguments = get_args()
	input_file_path = arguments.input_file_path

	preprocess(input_file_path)


if __name__ == "__main__":
	main()

