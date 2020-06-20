from utils import create_input_files

if __name__ == '__main__':
    # Create input files (along with word map)
    create_input_files(dataset='coco',
                       karpathy_json_path='./data1/json.json',
                       image_folder='./data1',
                       captions_per_image=5,
                       min_word_freq=5,
                       output_folder='/media/ssd/caption data1/',
                       max_len=50)
