import numpy as np
from csc.divisi2.operators import dot, multiply, aligned_matrix_multiply
from csc.divisi2.exceptions import LabelError, DimensionMismatch
from csc.divisi2.labels import LabeledMatrixMixin
from csc.divisi2.ordered_set import apply_indices
from csc.divisi2.sparse import SparseMatrix
from csc.divisi2.dense import DenseMatrix

SLICE_ALL = slice(None, None, None)

class ReconstructedMatrix(LabeledMatrixMixin):
    """
    Create a matrix from two factors that will only be multiplied together
    lazily. These factors can be DenseMatrices or SparseMatrices, as long
    as they match.

    This allows you to work with SVD results as if they are large dense
    matrices, without actually storing the large dense matrices.
    """
    ndim = 2

    def __init__(self, left, right, shifts=None):
        if not isinstance(left, (SparseMatrix, DenseMatrix)):
            left = DenseMatrix(left)
        if not isinstance(right, (SparseMatrix, DenseMatrix)):
            right = left.__class__(right)
        self.left = left
        self.right = right
        if self.left.shape[1] != self.right.shape[0]:
            raise DimensionMismatch("Inner dimensions do not match.")
        if self.left.col_labels != self.right.row_labels:
            if self.left.col_labels is None:
                raise LabelError("Can't multiply labeled with unlabeled data.")
            else:
                raise LabelError("Inner labels do not match.")

        self.row_labels = left.row_labels
        self.col_labels = right.col_labels
        self.shifts = shifts
        if not shifts:
            self.row_shift = np.zeros((self.shape[0],))
            self.col_shift = np.zeros((self.shape[1],))
            self.total_shift = 0.0
        else:
            assert len(shifts) == 3
            self.row_shift, self.col_shift, self.total_shift = shifts

    @property
    def shape(self):
        return (self.left.shape[0], self.right.shape[1])
    
    def transpose(self):
        return ReconstructedMatrix(self.right.T, self.left.T)

    @property
    def T(self):
        return self.transpose()
    
    def to_dense(self):
        return dot(self.left, self.right)

    def copy(self):
        return ReconstructedMatrix(self.left, self.right)
    
    def __getitem__(self, indices):
        if not isinstance(indices, tuple):
            indices = (indices,)
        if len(indices) < 2:
            indices += (SLICE_ALL,) * (2-len(indices))
        leftpart = self.left[indices[0], :]
        rightpart = self.right[:, indices[1]]
        if (not np.isscalar(indices[0])) and (not np.isscalar(indices[1])):
            # slice by slice. Reconstruct a new matrix to avoid huge
            # computations.
            return ReconstructedMatrix(leftpart, rightpart, self.shifts)
        else:
            # in any other case, just return the dense result
            row_shift = self.row_shift[indices[0]]
            col_shift = self.col_shift[indices[1]]
            return (dot(leftpart, rightpart) + row_shift + col_shift
                    + self.total_shift)

    def matvec(self, vec):
        return dot(self.left, dot(self.right, vec))

    def matvec_transp(self, vec):
        return dot(self.right.T, dot(self.left.T, vec))
    
    def left_category(self, vec):
        return dot(aligned_matrix_multiply(vec, self.left), self.right)
    left_adhoc_category = left_category

    def right_category(self, vec):
        return dot(self.left, aligned_matrix_multiply(self.right, vec))
    right_adhoc_category = right_category

    def __setitem__(self, indices, targetdata):
        # Random thought for the future:
        # Wouldn't it be neat if this did gradient descent? Then the
        # Hebbian incremental SVD would be an amazingly simple setitem loop.
        raise TypeError("Can't assign to entries of a ReconstructedMatrix")
    
    def evaluate_ranking(self, testdata):
        def order_compare(s1, s2):
            assert len(s1) == len(s2)
            score = 0.0
            total = 0
            for i in xrange(len(s1)):
                for j in xrange(i+1, len(s1)):
                    if s1[i] < s1[j]:
                        if s2[i] < s2[j]: score += 1
                        elif s2[i] > s2[j]: score -= 1
                        total += 1
                    elif s1[i] > s1[j]:
                        if s2[i] < s2[j]: score -= 1
                        elif s2[i] > s2[j]: score += 1
                        total += 1
            # move onto 0-1 scale
            score += (total-score)/2.0
            return (float(score) / total, score, total)
        
        values1 = []
        values2 = []
        row_labels = self.row_labels
        col_labels = self.col_labels
        for value, label1, label2 in testdata.named_entries():
            if label1 in row_labels and label2 in col_labels:
                values1.append(value)
                values2.append(self.entry_named(label1, label2))
        s1, s1s, s1t = order_compare(values1, values2)
        s2, s2s, s2t = order_compare(values1, values1)
        return s1s, s2s, s1/s2

    def evaluate_assertions(self, filename):
        """
        Evaluate the predictions that this matrix makes against a matrix of
        test data.

        This is kind of deprecated in favor of evaluate_ranking(), which does
        it more generally.
        """
        def order_compare(s1, s2):
            assert len(s1) == len(s2)
            score = 0.0
            total = 0
            for i in xrange(len(s1)):
                for j in xrange(i+1, len(s1)):
                    if s1[i] < s1[j]:
                        if s2[i] < s2[j]: score += 1
                        elif s2[i] > s2[j]: score -= 1
                        total += 1
                    elif s1[i] > s1[j]:
                        if s2[i] < s2[j]: score -= 1
                        elif s2[i] > s2[j]: score += 1
                        total += 1
            # move onto 0-1 scale
            score += (total-score)/2.0
            return (float(score) / total, score, total)
        
        from csc import divisi2
        testdata = divisi2.load(filename)
        values1 = []
        values2 = []
        row_labels = self.row_labels
        col_labels = self.col_labels
        for value, label1, label2 in testdata.named_entries():
            if label1 in row_labels and label2 in col_labels:
                values1.append(value)
                values2.append(self.entry_named(label1, label2))
        s1, s1s, s1t = order_compare(values1, values2)
        s2, s2s, s2t = order_compare(values1, values1)
        return s1s, s2s, s1/s2

    def __repr__(self):
        return "<ReconstructedMatrix: %d by %d>" % (self.shape[0], self.shape[1])

def reconstruct(u, s, v, shifts=None):
    """
    Reconstruct an approximation to the original matrix A from the SVD result
    (U, S, V).
    """
    return ReconstructedMatrix(u*s, v.T, shifts)

def reconstruct_symmetric(u):
    """
    Reconstruct the symmetrical matrix U * U^T.
    """
    return ReconstructedMatrix(u, u.T)

def reconstruct_similarity(u, s, post_normalize=True):
    """
    Reconstruct the symmetrical, weighted similarity matrix U * Sigma^2 * U^T.

    If `post_normalize` is true, then (U * Sigma) will be normalized so that
    the entries of the result are in the range [-1, 1].
    """
    mat = u*s
    if post_normalize: mat = mat.normalize_rows()
    return reconstruct_symmetric(mat)

def reconstruct_activation(V, S, post_normalize=True):
    """
    A square matrix can be decomposed as A = V * Lambda * V^T, where Lambda
    contains the eigenvalues of the matrix and V contains the eigenvectors.
    This is similar to the SVD, A = U * Sigma * V^T.

    In fact, if you take the SVD, you will get U = V and Sigma = Lambda^2.
    
    By exponentiating Lambda, we can turn our decomposition into an operator
    that simulates an infinite number of steps of spreading activation, with
    diminishing effects.
    
    This function takes in the SVD results V and Sigma (or, equivalently, U and
    Sigma), and reconstructs a spreading activation operator from them.
    """
    Lambda = np.sqrt(S)
    mat = (V * np.exp(Lambda/2))
    if post_normalize: mat = mat.normalize_rows()
    return reconstruct_symmetric(mat)
    
