# Title: main.py
# Authors: Sofiia Khutorna, Rem D'Ambrosio
# Created: 2024-07-09 
# Description: v0.1 (getting perl scipts) -> formatted data -> grabber -> training data -> trainer -> tester

from Grabber import Grabber
from Trainer import Trainer  
from Tester import Tester
import argparse
 

DATA_PATH = '../v0.2/databases'
SAMPLE_LEN = 14
LABEL = 'v0.2_date_range'
MODEL_PATH = '../v0.2/analyzing/models/ensemble1/model1.pt'
EPOCHS = 2000


def main():
    parser = argparse.ArgumentParser(description='building and training neural network')
    parser.add_argument('-gr', '--grab', action='store_true', help='grab all samples')
    parser.add_argument('-tr', '--train', action='store_true', help='training regular neural network')
    parser.add_argument('-te', '--test', action='store_true', help='testing nn model')
    args = parser.parse_args()

    if args.grab:
        grab()  
        
    if args.train:     
        train()

    if args.test:
        test()
  
  
def grab():
    print("Grabbing samples...")
    grabber = Grabber(DATA_PATH, SAMPLE_LEN)
    print("Writing to datasets...")
    grabber.samples_to_file(LABEL)
    print("===Datasets updated===\n")
  

def train():
    print("Training model...")
    trainer = Trainer(DATA_PATH)
       
    model = trainer.create_model()
    # model = trainer.load_model(MODEL_PATH)   

    trainer.train_model(model, EPOCHS)
    trainer.save_model(model, MODEL_PATH)
 

def test():
    print("Testing models...")
    tester = Tester(DATA_PATH)

    # model = tester.load_model(MODEL_PATH)
    # tester.test_model(model)
    
    ensemble_path = '../v0.2/analyzing/models/ensemble1/'
    models = tester.load_ensemble(ensemble_path)
    for i, model in enumerate(models):
        print(f'========== MODEL {i + 1} ==========')
        tester.test_model(model)
    print("========== ENSEMBLE RESULTS ==========")
    tester.test_ensemble(models)
  

if __name__ == '__main__':
    main()
