from __future__ import annotations

from functools import partial
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu, QWidget


class ScikitMenu(QMenu):
    def __init__(self, parent: QWidget | None = None):
        super().__init__('&skimage', parent)

        # Submenu for Blur
        blur = QMenu('Blur', self)

        callback = partial(parent.on_preview, 'scikit_bilateral')
        bilateral = QAction('Bilateral Filter', blur)
        bilateral.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_gaussian')
        gaussian = QAction('Gaussian Blur', blur)
        gaussian.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_median')
        median = QAction('Median Blur', blur)
        median.triggered.connect(callback)

        blur.addAction(bilateral)
        blur.addAction(gaussian)
        blur.addAction(median)

        self.addMenu(blur)

        # Submenu for Edge Detection
        edge_detection = QMenu('Edge Detection', self)

        callback = partial(parent.on_preview, 'scikit_canny')
        canny = QAction('Canny', edge_detection)
        canny.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_laplacian')
        laplacian = QAction('Laplacian', edge_detection)
        laplacian.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_scharr')
        scharr = QAction('Scharr', edge_detection)
        scharr.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_sobel')
        sobel = QAction('Sobel', edge_detection)
        sobel.triggered.connect(callback)

        edge_detection.addAction(canny)
        edge_detection.addAction(laplacian)
        edge_detection.addAction(scharr)
        edge_detection.addAction(sobel)

        self.addMenu(edge_detection)

        # Submenu for Feature Detection
        feature_detection = QMenu('Feature Detection', self)

        callback = partial(parent.on_preview, 'scikit_clahe')
        clahe = QAction('CLAHE', feature_detection)
        clahe.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_orb')
        orb = QAction('ORB', feature_detection)
        orb.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_sift')
        sift = QAction('SIFT', feature_detection)
        sift.triggered.connect(callback)

        feature_detection.addAction(clahe)
        feature_detection.addAction(orb)
        feature_detection.addAction(sift)

        self.addMenu(feature_detection)

        # Submenu for Morphological
        morphological = QMenu('Morphological', self)

        callback = partial(parent.on_preview, 'scikit_black_hat')
        black_hat = QAction('Black Hat', morphological)
        black_hat.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_closing')
        closing = QAction('Closing', morphological)
        closing.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_dilation')
        dilation = QAction('Dilation', morphological)
        dilation.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_erosion')
        erosion = QAction('Erosion', morphological)
        erosion.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_morphological_gradient')
        morphological_gradient = QAction('Morphological Gradient', morphological)
        morphological_gradient.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_opening')
        opening = QAction('Opening', morphological)
        opening.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_top_hat')
        top_hat = QAction('Top Hat', morphological)
        top_hat.triggered.connect(callback)

        morphological.addAction(black_hat)
        morphological.addAction(closing)
        morphological.addAction(dilation)
        morphological.addAction(erosion)
        morphological.addAction(morphological_gradient)
        morphological.addAction(opening)
        morphological.addAction(top_hat)

        self.addMenu(morphological)

        callback = partial(parent.on_preview, 'scikit_brightness')
        brightness = QAction('Brightness', self)
        brightness.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_contour')
        contour = QAction('Contour', self)
        contour.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_contrast')
        contrast = QAction('Contrast', self)
        contrast.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_difference_of_gaussians')
        difference_of_gaussians = QAction('Difference of Gaussians', self)
        difference_of_gaussians.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_histogram_equalization')
        histogram_equalization = QAction('Histogram Equalization', self)
        histogram_equalization.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_hough')
        hough = QAction('Hough Transform', self)
        hough.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_sharpen')
        sharpen = QAction('Sharpen', self)
        sharpen.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_superpixel_segmentation')
        superpixel_segmentation = QAction('Superpixel Segmentation', self)
        superpixel_segmentation.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_threshold')
        threshold = QAction('Threshold', self)
        threshold.triggered.connect(callback)

        self.addAction(brightness)
        self.addAction(contour)
        self.addAction(contrast)
        self.addAction(difference_of_gaussians)
        self.addAction(histogram_equalization)
        self.addAction(hough)
        self.addAction(sharpen)
        self.addAction(superpixel_segmentation)
        self.addAction(threshold)

        callback = partial(parent.on_preview, 'scikit_brightness')
        brightness = QAction('Brightness', self)
        brightness.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_contrast')
        contrast = QAction('Contrast', self)
        contrast.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_dbscan')
        dbscan = QAction('DBSCAN', self)
        dbscan.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_hog')
        hog = QAction('HOG', self)
        hog.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_skeletonize')
        skeletonize = QAction('Skeletonize', self)
        skeletonize.triggered.connect(callback)

        callback = partial(parent.on_preview, 'scikit_watershed')
        watershed = QAction('Watershed', self)
        watershed.triggered.connect(callback)

        self.addAction(brightness)
        self.addAction(contrast)
        self.addAction(dbscan)
        self.addAction(hog)
        self.addAction(skeletonize)
        self.addAction(watershed)
