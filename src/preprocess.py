import os
from typing import Dict
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


class Preprocess:
	"""Preprocess for dataframe."""
	def __init__(self, path: str, params: Dict) -> None:
		"""初期化"""
		self.path = path
		self.params = params

	@staticmethod
	def _load_data(path: str, params: Dict) -> pd.DataFrame:
		"""ファイルを読み込む.
		
		入力csvファイルをロードし、データフレームに変換する
		"""
		LOGGER.info(f"Load dataset from {path}.")
		if os.path.isfile(path):
			df = pd.read_csv(path, **params)
			return df
		else:
			raise ValueError(f"'{path}' is not exist, check the file path.")

	@staticmethod
	def _save_data(path: str, objects: pd.DataFrame):
		"""ファイルを保存する.
		
		データフレームを出力csvファイルに保存する
		"""
		LOGGER.info(f"Save dataset to {path}.")
		objects.to_csv(path, index=False)

	def run(self):
		"""前処理を実行する"""
		# データロード
		df = self._load_data(self.path, self.params)

		# 前処理
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

		# データを保存する
		output_file = os.path.splitext(self.path)[0] + "_preprocess.csv"
		self._save_data(output_file, df)


def main():
	"""Main function."""
	arguments = get_args()
	input_file_path = arguments.input_file_path
	params = {
		"skiprows": 1,
		"header": 0
	}

	# 前処理
	preprocess = Preprocess(input_file_path, params)
	preprocess.run()


if __name__ == "__main__":
	main()

