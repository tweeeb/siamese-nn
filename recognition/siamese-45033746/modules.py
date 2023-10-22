import torch.nn as nn


class SiameseNetwork(nn.Module):
    """
    Siamese CNN
    Reference: https://github.com/maticvl/dataHacker/blob/master/pyTorch/014_siameseNetwork.ipynb
    """

    def __init__(self):
        super(SiameseNetwork, self).__init__()

        self.cnn1 = nn.Sequential(
            nn.Conv2d(1, 32, 11, 1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(32, 64, 5, 1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(64, 128, 3, 1),
            nn.ReLU(inplace=True),
        )

        self.fc1 = nn.Sequential(
            nn.Linear(128, 512),
            nn.ReLU(inplace=True),

            nn.Linear(512, 256),
            nn.ReLU(inplace=True),

            nn.Linear(256, 2)
        )

    def forward_once(self, tensor):
        # This function will be called on each of the triplet in forward()
        # It's output is used to determine the similiarity
        # REDO
        cnn_output = self.cnn1(tensor)
        print(tensor.size())
        cnn_output = cnn_output.view(cnn_output.size()[0], -1)
        print(tensor.size())
        cnn_output = self.fc1(cnn_output)
        return cnn_output

    def forward(self, anchor, positive, negative):
        # In this function we pass in  triplet images and obtain triplet vectors
        # which are returned
        # REDO
        anchor_vec = self.forward_once(anchor)
        positive_vec = self.forward_once(positive)
        negative_vec = self.forward_once(negative)

        return anchor_vec, positive_vec, negative_vec


if __name__ == "__main__":
    pass
