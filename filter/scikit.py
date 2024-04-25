from __future__ import annotations

import numpy as np
import numpy.typing as npt
import random

from constant import COLOR
from filter.base import BaseFilter
from scipy import ndimage as ndi
from skimage import exposure
from skimage import measure
from sklearn.cluster import DBSCAN
from skimage.feature import (
    canny,
    hog,
    ORB,
    peak_local_max,
    SIFT
)
from skimage.filters import (
    gaussian,
    laplace,
    median,
    scharr,
    sobel,
    threshold_local,
    threshold_otsu,
    unsharp_mask
)
from skimage.measure import label
from skimage.morphology import (
    binary_erosion,
    binary_dilation,
    dilation,
    erosion,
    skeletonize
)
from skimage.restoration import denoise_bilateral
from skimage.segmentation import slic, watershed
from skimage.transform import probabilistic_hough_line


class ScikitBilateralFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'bilateral_filter'

    def __repr__(self) -> str:
        return 'bilateral_filter'

    def __str__(self) -> str:
        return 'bilateral_filter'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        sigma_color = self.parameter.get('sigma_color', 1.0)
        sigma_spatial = self.parameter.get('sigma_spatial', 1.0)

        return denoise_bilateral(
            image,
            sigma_color=sigma_color,
            sigma_spatial=sigma_spatial
        )


class ScikitBlackHatFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'black_hat'

    def __repr__(self) -> str:
        return 'black_hat'

    def __str__(self) -> str:
        return 'black_hat'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        iterations = self.parameter.get('iterations', 1)

        binary = (image > 128).astype(bool)

        original = binary.copy()

        for _ in range(iterations):
            binary = binary_dilation(binary)

        for _ in range(iterations):
            binary = binary_erosion(binary)

        result = np.logical_xor(original, binary)

        return result.astype(np.uint8) * 255


class ScikitBrightnessFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'brightness'

    def __repr__(self) -> str:
        return 'brightness'

    def __str__(self) -> str:
        return 'brightness'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        gamma = self.parameter.get('gamma', 1.0)
        return exposure.adjust_gamma(image, gamma=gamma)


class ScikitCannyFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'canny'

    def __repr__(self) -> str:
        return 'canny'

    def __str__(self) -> str:
        return 'canny'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        sigma = self.parameter.get('sigma', 1.0)
        low_threshold = self.parameter.get('low_threshold', 0.1)
        high_threshold = self.parameter.get('high_threshold', 0.2)

        return canny(
            image,
            sigma=sigma,
            low_threshold=low_threshold,
            high_threshold=high_threshold
        )


class ScikitCLAHEFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'clahe'

    def __repr__(self) -> str:
        return 'clahe'

    def __str__(self) -> str:
        return 'clahe'

    def apply(self, image: np.ndarray) -> np.ndarray:
        clip_limit = self.parameter.get('clip_limit', 0.01)
        kernel_size = self.parameter.get('grid_size', (8, 8))

        return exposure.equalize_adapthist(
            image,
            clip_limit=clip_limit,
            kernel_size=kernel_size
        )


class ScikitClosingFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'closing'

    def __repr__(self) -> str:
        return 'closing'

    def __str__(self) -> str:
        return 'closing'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        iterations = self.parameter.get('iterations', 1)

        binary = (image > 128).astype(bool)

        for _ in range(iterations):
            binary = binary_erosion(binary)

        for _ in range(iterations):
            binary = binary_dilation(binary)

        return binary.astype(np.uint8) * 255


class ScikitContourFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'contour'

    def __repr__(self) -> str:
        return 'contour'

    def __str__(self) -> str:
        return 'contour'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        return measure.find_contours(image, 0.5)


class ScikitContrastFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'contrast'

    def __repr__(self) -> str:
        return 'contrast'

    def __str__(self) -> str:
        return 'contrast'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        contrast = self.parameter.get('contrast', 1.0)

        adjusted = exposure.rescale_intensity(
            image,
            in_range='image',
            out_range='dtype'
        )

        return adjusted * contrast


class ScikitDBSCANFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'dbscan'

    def __repr__(self) -> str:
        return 'dbscan'

    def __str__(self) -> str:
        return 'dbscan'

    def apply(self, image: np.ndarray) -> np.ndarray:
        eps = self.parameter.get('epsilon', 10)
        min_samples = self.parameter.get('min_samples', 5)

        if image.ndim == 3 and image.shape[2] == 3:
            flat = image.reshape(-1, 3)
        elif image.ndim == 2:
            flat = np.repeat(image[:, :, np.newaxis], 3, axis=2).reshape(-1, 3)
        else:
            message = 'Unsupported image format'
            raise ValueError(message)

        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(flat)

        clustered = np.array(
            [
                COLOR[label]
                if label != -1 else COLOR[0]
                for label in labels
            ]
        )

        if image.ndim == 2:
            return clustered.reshape(
                image.shape[0],
                image.shape[1],
                3
            )

        return clustered.reshape(image.shape)


class ScikitDifferenceOfGaussiansFilter(BaseFilter):
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

        first = gaussian(image, sigma=sigma1)
        second = gaussian(image, sigma=sigma2)

        return first - second


class ScikitDilationFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'dilation'

    def __repr__(self) -> str:
        return 'dilation'

    def __str__(self) -> str:
        return 'dilation'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        footprint = self.parameter.get('selem', None)

        if footprint is None:
            footprint = np.ones((3, 3), dtype=bool)

        binary = (image > 128).astype(bool)
        return dilation(binary, footprint=footprint).astype(np.uint8) * 255


class ScikitErosionFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'erosion'

    def __repr__(self) -> str:
        return 'erosion'

    def __str__(self) -> str:
        return 'erosion'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        footprint = self.parameter.get('selem', None)

        if footprint is None:
            footprint = np.ones((3, 3), dtype=bool)

        binary = (image > 128).astype(bool)
        return erosion(binary, footprint=footprint).astype(np.uint8) * 255


class ScikitGaussianBlurFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'gaussian_blur'

    def __repr__(self) -> str:
        return 'gaussian_blur'

    def __str__(self) -> str:
        return 'gaussian_blur'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        sigma = self.parameter.get('sigma', 1.0)

        return gaussian(image, sigma=sigma)


class ScikitHistogramEqualizationFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'histogram_equalization'

    def __repr__(self) -> str:
        return 'histogram_equalization'

    def __str__(self) -> str:
        return 'histogram_equalization'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        return exposure.equalize_hist(image)


class ScikitHOGFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'hog'

    def __repr__(self) -> str:
        return 'hog'

    def __str__(self) -> str:
        return 'hog'

    def apply(self, image: np.ndarray) -> np.ndarray:
        orientations = self.parameter.get('orientation', 1)

        _, result = hog(
            image,
            orientations=orientations,
            pixels_per_cell=(16, 16),
            cells_per_block=(1, 1),
            visualize=True,
        )

        return result


class ScikitHoughTransformFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'hough'

    def __repr__(self) -> str:
        return 'hough'

    def __str__(self) -> str:
        return 'hough'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        threshold = self.parameter.get('threshold', 10)
        line_length = self.parameter.get('line_length', 5)
        line_gap = self.parameter.get('line_gap', 3)

        return probabilistic_hough_line(
            image,
            threshold=threshold,
            line_length=line_length,
            line_gap=line_gap
        )


class ScikitLaplacianFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'laplacian'

    def __repr__(self) -> str:
        return 'laplacian'

    def __str__(self) -> str:
        return 'laplacian'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        return laplace(image)


class ScikitMedianBlurFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'median_blur'

    def __repr__(self) -> str:
        return 'median_blur'

    def __str__(self) -> str:
        return 'median_blur'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        kernel_size = self.parameter.get('kernel_size', 3)
        footprint = np.ones((kernel_size, kernel_size))

        return median(
            image,
            footprint=footprint
        )


class ScikitMorphologicalGradientFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'morphological_gradient'

    def __repr__(self) -> str:
        return 'morphological_gradient'

    def __str__(self) -> str:
        return 'morphological_gradient'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        erosion = binary_erosion(image)
        dilation = binary_dilation(image)

        return dilation - erosion


class ScikitOpeningFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'opening'

    def __repr__(self) -> str:
        return 'opening'

    def __str__(self) -> str:
        return 'opening'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        iterations = self.parameter.get('iterations', 1)

        binary = (image > 128).astype(bool)

        for _ in range(iterations):
            binary = binary_erosion(binary)

        for _ in range(iterations):
            binary = binary_dilation(binary)

        return binary.astype(np.uint8) * 255


class ScikitORBFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'orb'

    def __repr__(self) -> str:
        return 'orb'

    def __str__(self) -> str:
        return 'orb'

    def apply(self, image: np.ndarray) -> np.ndarray:
        orb = ORB()

        orb.detect_and_extract(image)
        keypoints = orb.keypoints
        descriptors = orb.descriptors

        return keypoints, descriptors


class ScikitScharrFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'scharr_operator'

    def __repr__(self) -> str:
        return 'scharr_operator'

    def __str__(self) -> str:
        return 'scharr_operator'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        return scharr(image)


class ScikitSIFTFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'sift'

    def __repr__(self) -> str:
        return 'sift'

    def __str__(self) -> str:
        return 'sift'

    def apply(self, image: np.ndarray) -> np.ndarray:
        sift = SIFT()

        keypoints, descriptors = sift.detect_and_compute(image)
        return keypoints, descriptors


class ScikitSharpenFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'sharpen'

    def __repr__(self) -> str:
        return 'sharpen'

    def __str__(self) -> str:
        return 'sharpen'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        alpha = self.parameter.get('alpha', 1.5)
        amount = self.parameter.get('amount', 1.0)

        return unsharp_mask(image, radius=alpha, amount=amount)


class ScikitSkeletonizeFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'skeletonize'

    def __repr__(self) -> str:
        return 'skeletonize'

    def __str__(self) -> str:
        return 'skeletonize'

    def apply(self, image: np.ndarray) -> np.ndarray:
        binary = (image > 0).astype(np.uint8)
        return skeletonize(binary)


class ScikitSobelFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'sobel'

    def __repr__(self) -> str:
        return 'sobel'

    def __str__(self) -> str:
        return 'sobel'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        return sobel(image)


class ScikitSuperpixelSegmentationFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'superpixel_segmentation'

    def __repr__(self) -> str:
        return 'superpixel_segmentation'

    def __str__(self) -> str:
        return 'superpixel_segmentation'

    def apply(self, image: np.ndarray) -> np.ndarray:
        n_segments = self.parameter.get('n_segments', 100)
        compactness = self.parameter.get('compactness', 1.0)

        return slic(
            image,
            channel_axis=None,
            n_segments=n_segments,
            compactness=compactness
        )


class ScikitThresholdFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'threshold'

    def __repr__(self) -> str:
        return 'threshold'

    def __str__(self) -> str:
        return 'threshold'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        threshold_method = self.parameter.get('method', 'otsu')
        block_size = self.parameter.get('block_size', 35)
        offset = self.parameter.get('offset', 0)

        if threshold_method == 'otsu':
            threshold_value = threshold_otsu(image)
            thresholded_image = image > threshold_value
        elif threshold_method == 'local':
            thresholded_image = threshold_local(image, block_size, offset=offset)

        return thresholded_image


class ScikitTopHatFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'top_hat'

    def __repr__(self) -> str:
        return 'top_hat'

    def __str__(self) -> str:
        return 'top_hat'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        iterations = self.parameter.get('iterations', 1)

        binary = (image > 128).astype(bool)
        original = binary.copy()

        for _ in range(iterations):
            binary = binary_erosion(binary)

        for _ in range(iterations):
            binary = binary_dilation(binary)

        result = np.logical_xor(original, binary)
        return result.astype(np.uint8) * 255


class ScikitWatershedFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'watershed'

    def __repr__(self) -> str:
        return 'watershed'

    def __str__(self) -> str:
        return 'watershed'

    def apply(self, image: np.ndarray) -> np.ndarray:
        marker_option = self.parameter.get('marker_option', 'peak_local_max')
        num_peaks = self.parameter.get('markers', 10)
        connectivity = self.parameter.get('connectivity', 1)

        if image.ndim == 3 and image.shape[2] == 3:
            image = np.mean(image, axis=2)

        # Generate markers
        distance = ndi.distance_transform_edt(image)

        match marker_option:
            case 'peak_local_max':
                local_maxi = peak_local_max(
                    distance,
                    footprint=np.ones((3, 3)),
                    labels=image,
                    num_peaks=num_peaks
                )

                markers = label(local_maxi)

                expanded_markers = np.zeros_like(image, dtype=np.int32)

                for marker_idx, coords in enumerate(local_maxi, start=1):
                    expanded_markers[coords[0], coords[1]] = marker_idx

                markers = expanded_markers
            case 'otsu_thresholding':
                thresh = threshold_otsu(image)
                markers = np.zeros_like(image)
                markers[image > thresh] = 1
                markers = label(markers)
            case 'distance_transform':
                distance = ndi.distance_transform_edt(image)
                markers = label(distance > distance.mean())
            case 'manual':
                markers = self.parameter.get(
                    'manual',
                    np.zeros_like(image, dtype=np.int32)
                )
            case 'random':
                markers_count = self.parameter.get('markers', 10)
                expanded_markers = np.zeros_like(image, dtype=np.int32)

                for m in range(1, markers_count + 1):
                    x, y = (
                        random.randint(0, image.shape[0] - 1),
                        random.randint(0, image.shape[1] - 1)
                    )

                    expanded_markers[x, y] = m

                markers = expanded_markers

        # Apply Watershed
        labels = watershed(
            -distance,
            markers,
            mask=image,
            connectivity=connectivity
        )

        # Color the segments - this is just for visualization
        segmented = np.zeros(
            (image.shape[0], image.shape[1], 3),
            dtype=np.uint8
        )

        for label_id in np.unique(labels):
            if label_id == 0:
                continue

            segmented[labels == label_id] = np.random.randint(0, 255, 3)

        return segmented
