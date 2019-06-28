from scipy.sparse import coo_matrix
import numpy as np
import matplotlib.pyplot as plt

def main():

    mat = np.loadtxt('LGN.txt')
    sp_mat = coo_matrix((np.log(1+np.log((mat[:,2]))), (mat[:,0], mat[:,1])), shape=(442,442))

    plt.imshow(sp_mat.toarray(), cmap='gray_r')
    plt.savefig('LGN_mat.png')

if __name__ == '__main__':
    main()
