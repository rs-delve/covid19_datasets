from covid19_datasets import Combined
import pandas as pd

import logging
_log = logging.getLogger(__name__)


OUTPUT_FILENAME = './dataset/combined_dataset_latest.csv'


def main():
	_log.info('Generating combined dataset')
	combined = Combined()
	data = combined.get_data()
	data.to_csv(OUTPUT_FILENAME)
	_log.info('Wrote output to: ' + OUTPUT_FILENAME)



if __name__ == '__main__':
    main()
