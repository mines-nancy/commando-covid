import numpy as np

from kernels.abstract_kernel import Kernel


class GaussianLinearKernel(Kernel):
    def __init__(self,
                 log_amplitude_gaussian: float,
                 log_length_scale: float,
                 log_noise_scale: float,
                 log_amplitude_linear: float,
                 log_offset:float,
                 c: float
                 ):
        super(GaussianLinearKernel, self).__init__(log_amplitude_gaussian,
                                                   log_length_scale,
                                                   log_noise_scale,
                                                   )
        self.log_amplitude_linear = log_amplitude_linear
        self.c = c
        self.log_offset = log_offset

    @property
    def amplitude_linear_squared(self):
        return np.exp(self.log_amplitude * 2)

    @property
    def offset_squared(self):
        return np.exp(self.log_offset * 2)

    def get_covariance_matrix(self,
                              X: np.ndarray,
                              Y: np.ndarray,
                              ) -> np.ndarray:
        """
        :param X: numpy array of size n_1 x m for which each row (x_i) is a data point at which the objective function can be evaluated
        :param Y: numpy array of size n_2 x m for which each row (y_j) is a data point at which the objective function can be evaluated
        :return: numpy array of size n_1 x n_2 for which the value at position (i, j) corresponds to the value of
        k(x_i, y_j), where k represents the kernel used.
        """



        distances_array = np.array([[np.linalg.norm(x_p - x_q) for x_q in Y] for x_p in X])
        covariance_matrix = (
                self.amplitude_squared
                * np.exp((-1 / (2 * self.length_scale ** 2))
                         * (distances_array ** 2))
        ) + self.amplitude_linear_squared * (X - self.c).dot(Y.T - self.c) + self.offset_squared

        return covariance_matrix

    def set_parameters(self,
                       log_amplitude: float,
                       log_length_scale: float,
                       log_noise_scale: float,
                       log_amplitude_linear=0,
                       c=0,
                       log_offset=0,
                       ) -> None:
        self.log_amplitude_linear = log_amplitude_linear
        self.c = c
        self.log_offset = log_offset
        super(GaussianLinearKernel, self).set_parameters(log_amplitude, log_length_scale, log_noise_scale)


    def __call__(self,
                 X: np.ndarray,
                 Y: np.ndarray,
                 ) -> np.ndarray:
        return self.get_covariance_matrix(X, Y)
