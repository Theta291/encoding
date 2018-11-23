git clone -b huff https://github.com/Theta291/encoding.git
conda env create -f ./encoding/huff-coding-explanation/huff-ipynb-env.yml
source activate huff-coding
jupyter notebook ./encoding/huff-coding-explanation/huffman-coding.ipynb
