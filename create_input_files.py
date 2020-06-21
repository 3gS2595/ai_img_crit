from pip._vendor.distlib._backport import shutil

from utils import create_input_files

if __name__ == '__main__':
    # Create input files (along with word map)
    shutil.rmtree(/home/clem/PycharmProjects/TheSaltzWaltz/output)
    create_input_files(dataset='coco',
                       karpathy_json_path='./crawlers/output/JSON.json',
                       image_folder='',
                       captions_per_image=5,
                       min_word_freq=2,
                       output_folder='./output',
                       max_len=50)
