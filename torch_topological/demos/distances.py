"""Demo for distance minimisations of a point cloud."""


import logging

from torch_topological.nn import VietorisRips
from torch_topological.nn import WassersteinDistance

from torch_topological.utils import make_disk

import torch
import torch.optim as optim


import matplotlib.pyplot as plt


if __name__ == '__main__':
    n = 100

    X = make_disk(r=0.5, R=0.6, n=n)
    Y = make_disk(r=0.9, R=1.0, n=n)

    X = torch.nn.Parameter(torch.as_tensor(X), requires_grad=True)

    vr = VietorisRips(dim=1)

    pi_target = vr(Y)
    loss_fn = WassersteinDistance(q=2)

    opt = optim.SGD([X], lr=0.1)

    logging.basicConfig(
        level=logging.INFO
    )

    losses = []

    for i in range(500):

        opt.zero_grad()

        pi_source = vr(X)
        loss = loss_fn(pi_source, pi_target)

        loss.backward()
        opt.step()

        logging.info(loss.item())
        losses.append(loss.item())

    X = X.detach().numpy()

    plt.scatter(X[:, 0], X[:, 1], label='Source')
    plt.scatter(Y[:, 0], Y[:, 1], label='Target')

    plt.legend()
    plt.show()

