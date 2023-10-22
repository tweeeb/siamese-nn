from modules import BinaryClassifier, SiameseNetwork
from torch.utils.data import DataLoader
from os.path import exists
from train import BINARY_MODEL_PATH, SIAMESE_MODEL_PATH
import torch
from dataset import get_test_set
import torch.nn as nn

"""
predict.py

load trained models and measure accuracy
"""


def load():
    """
    Load pre-trained SiameseNet and BinaryClassifier models and predict
    :return:
    """
    # Device configuration
    gpu = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    if not exists(BINARY_MODEL_PATH) or not exists(SIAMESE_MODEL_PATH):
        print("No trained models available, please run train.py to create trained models")
        return

    bin_net = BinaryClassifier()
    bin_net.load_state_dict(torch.load(BINARY_MODEL_PATH))
    bin_net.to(gpu)

    siamese_net = SiameseNetwork()
    siamese_net.load_state_dict(torch.load(SIAMESE_MODEL_PATH))
    siamese_net.to(gpu)

    return bin_net, siamese_net, gpu


def predict(model: BinaryClassifier, net: SiameseNetwork, testDataLoader: DataLoader, device):
    model.eval()
    net.eval()

    outcome = []

    for i, (anchor_class, anchor, _, _) in enumerate(testDataLoader, 0):
        # Send items to GPU
        anchor, label = anchor.to(device), torch.unsqueeze(anchor_class.to(device), dim=1).float()

        # Get siamese embeddings for the input anchor image
        siamese_embeddings = net.forward_once(anchor)

        """
        none of this works, apologies, the sigmoid functon would not work to expectations
        """
        pred = model(siamese_embeddings)
        print(pred)



        outcome.append(torch.eq(pred, label))

    print(outcome)


def main():
    test = get_test_set()
    vals = load()
    if vals is None:
        return
    binnn, sin, device = vals
    predict(binnn, sin, test, device)


if __name__ == "__main__":
    main()
