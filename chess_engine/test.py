import numpy as np

rows,cols = (8,8)
board = list()

def createBoardCoordinate():
    for i in range(rows):
        row = []
        for j in range(cols):   
            row.append(j)
        board.append(row)

createBoardCoordinate()
board = np.array(board)
print(board)

# Convert (row, col) to flat index
row, col = 1, 2  # element 60
flat_index = np.ravel_multi_index((row, col), board.shape)
print(f"Flat index of ({row}, {col}):", flat_index)

# Convert flat index back to (row, col)
coords = np.unravel_index(flat_index, board.shape)
print(f"Coordinates of flat index {flat_index}:", coords)
