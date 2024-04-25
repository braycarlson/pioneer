from __future__ import annotations

import cv2
import numpy as np
import numpy.typing as npt

from filter.base import BaseFilter


class OpenCVBilateralFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'bilateral_filter'

    def __repr__(self) -> str:
        return 'bilateral_filter'

    def __str__(self) -> str:
        return 'bilateral_filter'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        d = self.parameter.get('diameter', 1)
        sigma_color = self.parameter.get('sigma_color', 1)
        sigma_space = self.parameter.get('sigma_space', 1)

        return cv2.bilateralFilter(image, d, sigma_color, sigma_space)


class OpenCVBlackHatFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'black_hat'

    def __repr__(self) -> str:
        return 'black_hat'

    def __str__(self) -> str:
        return 'black_hat'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        kernel_size = self.parameter.get('kernel_size', 3)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        return cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)


class OpenCVBrightnessFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'brightness'

    def __repr__(self) -> str:
        return 'brightness'

    def __str__(self) -> str:
        return 'brightness'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        amount = self.parameter.get('amount', 0)
        array = np.full_like(image, amount)
        return cv2.add(image, array)


class OpenCVCannyFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'canny'

    def __repr__(self) -> str:
        return 'canny'

    def __str__(self) -> str:
        return 'canny'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        lower_threshold = self.parameter.get('lower_threshold', 1)
        upper_threshold = self.parameter.get('upper_threshold', 10)

        return cv2.Canny(image, lower_threshold, upper_threshold)


class OpenCVCLAHEFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'clahe'

    def __repr__(self) -> str:
        return 'clahe'

    def __str__(self) -> str:
        return 'clahe'

    def apply(self, image: np.ndarray) -> np.ndarray:
        clip_limit = self.parameter.get('clip_limit', 1.0)
        grid_size = self.parameter.get('grid_size', 1)

        clahe = cv2.createCLAHE(
            clipLimit=clip_limit,
            tileGridSize=(grid_size, grid_size)
        )

        return clahe.apply(image)


class OpenCVClosingFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'closing'

    def __repr__(self) -> str:
        return 'closing'

    def __str__(self) -> str:
        return 'closing'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        kernel_size = self.parameter.get('kernel_size', 1)

        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)


class OpenCVContourFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'contour'

    def __repr__(self) -> str:
        return 'contour'

    def __str__(self) -> str:
        return 'contour'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        threshold_type = self.parameter.get('threshold_type')
        threshold = self.parameter.get('threshold', 1)
        retrieval_mode = self.parameter.get('retrieval_mode')
        approximation_mode = self.parameter.get('approximation_mode')

        if len(image.shape) == 2 or image.shape[2] == 1:
            grayscale = image
        else:
            grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        _, image = cv2.threshold(grayscale, threshold, 255, threshold_type)
        contour, _ = cv2.findContours(image, retrieval_mode, approximation_mode)
        return cv2.drawContours(image.copy(), contour, -1, (0, 255, 0), 3)


class OpenCVContrastFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'contrast'

    def __repr__(self) -> str:
        return 'contrast'

    def __str__(self) -> str:
        return 'contrast'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        amount = self.parameter.get('amount', 1.0)

        mean = np.mean(image)

        return cv2.addWeighted(
            image,
            amount,
            image,
            0,
            mean * (1 - amount)
        )


class OpenCVDifferenceOfGaussiansFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'difference_of_gaussians'

    def __repr__(self) -> str:
        return 'difference_of_gaussians'

    def __str__(self) -> str:
        return 'difference_of_gaussians'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        sigma1 = self.parameter.get('sigma1', 1.0)
        sigma2 = self.parameter.get('sigma2', 2.0)

        first = cv2.GaussianBlur(image, (0, 0), sigma1)
        second = cv2.GaussianBlur(image, (0, 0), sigma2)

        return first - second


class OpenCVDilationFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'dilation'

    def __repr__(self) -> str:
        return 'dilation'

    def __str__(self) -> str:
        return 'dilation'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        kernel_size = self.parameter.get('kernel_size', 1)
        iterations = self.parameter.get('iterations', 1)

        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.dilate(image, kernel, iterations=iterations)


class OpenCVErosionFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'erosion'

    def __repr__(self) -> str:
        return 'erosion'

    def __str__(self) -> str:
        return 'erosion'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        kernel_size = self.parameter.get('kernel_size', 1)
        iterations = self.parameter.get('iterations', 1)

        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.erode(image, kernel, iterations=iterations)


class OpenCVGaussianBlurFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'gaussian_blur'

    def __repr__(self) -> str:
        return 'gaussian_blur'

    def __str__(self) -> str:
        return 'gaussian_blur'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        kernel_size = self.parameter.get('kernel_size', 1)

        kernel_size = (
            kernel_size + 1
            if kernel_size % 2 == 0
            else kernel_size
        )

        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)


class OpenCVHistogramEqualizationFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'histogram_equalization'

    def __repr__(self) -> str:
        return 'histogram_equalization'

    def __str__(self) -> str:
        return 'histogram_equalization'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        return cv2.equalizeHist(image)


class OpenCVHoughTransformFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'hough'

    def __repr__(self) -> str:
        return 'hough'

    def __str__(self) -> str:
        return 'hough'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        rho = self.parameter.get('rho', 1)
        theta = self.parameter.get('theta', np.pi / 180)
        threshold = self.parameter.get('threshold', 100)

        # Perform Hough Line Transform
        lines = cv2.HoughLines(image, rho, theta, threshold)

        if lines is not None:
            for line in lines:
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

        return image


class OpenCVLaplacianFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'laplacian'

    def __repr__(self) -> str:
        return 'laplacian'

    def __str__(self) -> str:
        return 'laplacian'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        destination_depth = self.parameter.get('destination_depth', cv2.CV_64F)
        ksize = self.parameter.get('kernel_size', 1)

        return cv2.Laplacian(image, destination_depth, ksize=ksize)


class OpenCVMedianBlurFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'median_blur'

    def __repr__(self) -> str:
        return 'median_blur'

    def __str__(self) -> str:
        return 'median_blur'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        kernel_size = self.parameter.get('kernel_size', 1)

        kernel_size = (
            kernel_size + 1
            if kernel_size % 2 == 0
            else kernel_size
        )

        return cv2.medianBlur(image, kernel_size)


class OpenCVMorphologicalGradientFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'morphological_gradient'

    def __repr__(self) -> str:
        return 'morphological_gradient'

    def __str__(self) -> str:
        return 'morphological_gradient'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        kernel_size = self.parameter.get('kernel_size', 3)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        return cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)


class OpenCVOpeningFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'opening'

    def __repr__(self) -> str:
        return 'opening'

    def __str__(self) -> str:
        return 'opening'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        kernel_size = self.parameter.get('kernel_size', 1)

        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


class OpenCVORBFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'orb'

    def __repr__(self) -> str:
        return 'orb'

    def __str__(self) -> str:
        return 'orb'

    def apply(self, image: np.ndarray) -> np.ndarray:
        nfeatures = self.parameter.get('max_features', 1)

        orb = cv2.ORB_create(nfeatures=nfeatures)
        keypoints, _ = orb.detectAndCompute(image, None)
        return cv2.drawKeypoints(image, keypoints, None)


class OpenCVScharrFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'scharr_operator'

    def __repr__(self) -> str:
        return 'scharr_operator'

    def __str__(self) -> str:
        return 'scharr_operator'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        dx = self.parameter.get('dx', 1)
        dy = self.parameter.get('dy', 0)
        scale = self.parameter.get('scale', 1)
        delta = self.parameter.get('delta', 0)
        border_type = self.parameter.get('border_type', cv2.BORDER_DEFAULT)

        if dx < 0:
            dx = 0

        if dy < 0:
            dy = 0

        if dx + dy == 0:
            dy = 1

        return cv2.Scharr(
            image,
            cv2.CV_64F,
            dx,
            dy,
            scale=scale,
            delta=delta,
            borderType=border_type
        )


class OpenCVSIFTFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'sift'

    def __repr__(self) -> str:
        return 'sift'

    def __str__(self) -> str:
        return 'sift'

    def apply(self, image: np.ndarray) -> np.ndarray:
        sift = cv2.SIFT_create()
        keypoints, _ = sift.detectAndCompute(image, None)
        return cv2.drawKeypoints(image, keypoints, None)


class OpenCVSharpenFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'sharpen'

    def __repr__(self) -> str:
        return 'sharpen'

    def __str__(self) -> str:
        return 'sharpen'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        amount = self.parameter.get('amount', 0)

        kernel = np.array([
            [-1, -1, -1],
            [-1,  9, -1],
            [-1, -1, -1]
        ])

        sharp = cv2.filter2D(image, -1, kernel)

        return cv2.addWeighted(
            image,
            1 + amount / 100,
            sharp,
            -amount / 100, 0
        )


class OpenCVSkeletonizeFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'skeletonize'

    def __repr__(self) -> str:
        return 'skeletonize'

    def __str__(self) -> str:
        return 'skeletonize'

    def apply(self, image: np.ndarray) -> np.ndarray:
        _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

        return cv2.ximgproc.thinning(
            binary,
            thinningType=cv2.ximgproc.THINNING_GUOHALL
        )


class OpenCVSobelFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'sobel_edge_detection'

    def __repr__(self) -> str:
        return 'sobel_edge_detection'

    def __str__(self) -> str:
        return 'sobel_edge_detection'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        destination_depth = self.parameter.get('destination_depth')
        dx = self.parameter.get('dx', 1)
        dy = self.parameter.get('dy', 0)
        ksize = self.parameter.get('kernel_size', 1)

        if dx < 0:
            dx = 0

        if dy < 0:
            dy = 0

        if dx + dy == 0:
            dy = 1

        edges_x = cv2.Sobel(image, destination_depth, dx, dy, ksize=ksize)
        edges_y = cv2.Sobel(image, destination_depth, dx, dy, ksize=ksize)

        return np.sqrt(edges_x**2 + edges_y**2)


class OpenCVSuperpixelSegmentationFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'superpixel_segmentation'

    def __repr__(self) -> str:
        return 'superpixel_segmentation'

    def __str__(self) -> str:
        return 'superpixel_segmentation'

    def apply(self, image: np.ndarray) -> np.ndarray:
        num_superpixels = self.parameter.get('num_superpixels', 100)
        compactness = self.parameter.get('compactness', 10.0)

        if len(image.shape) == 2 or image.shape[2] == 1:
            color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        else:
            color = image.copy()

        slic = cv2.ximgproc.createSuperpixelSLIC(
            image,
            region_size=num_superpixels,
            ruler=compactness
        )

        slic.iterate(10)

        labels = slic.getLabels()
        labels_8uc1 = np.uint8(labels)
        color = cv2.applyColorMap(labels_8uc1, cv2.COLORMAP_JET)

        return cv2.addWeighted(color, 0.7, color, 0.3, 0)


class OpenCVThresholdFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'threshold'

    def __repr__(self) -> str:
        return 'threshold'

    def __str__(self) -> str:
        return 'threshold'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        method = self.parameter.get('method')
        argument = self.parameter.get('argument')
        threshold = self.parameter.get('threshold', 127)
        block_size = self.parameter.get('block_size', 11)
        c = self.parameter.get('c', 2)

        match method:
            case 'Otsu\'s Binarization':
                _, result = cv2.threshold(
                    image,
                    0,
                    255,
                    argument
                )
            case 'Adaptive Mean':
                result = cv2.adaptiveThreshold(
                    image,
                    255,
                    cv2.ADAPTIVE_THRESH_MEAN_C,
                    argument,
                    block_size,
                    c
                )
            case 'Adaptive Gaussian':
                result = cv2.adaptiveThreshold(
                    image,
                    255,
                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    argument,
                    block_size,
                    c
                )
            case _:
                _, result = cv2.threshold(
                    image,
                    threshold,
                    255,
                    argument
                )

        return result


class OpenCVTopHatFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'top_hat'

    def __repr__(self) -> str:
        return 'top_hat'

    def __str__(self) -> str:
        return 'top_hat'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        kernel_size = self.parameter.get('kernel_size', 3)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        return cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)
