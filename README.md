📌 Project Overview
Skin diseases affect over 900 million people globally. While many conditions are manageable, malignant melanoma accounts for nearly 75% of skin-cancer-related deaths. Early detection is critical; the 5-year survival rate drops from 98% (Stage I) to below 20% (Stage IV).

This project presents a rigorous comparative study of five generations of Convolutional Neural Network (CNN) architectures to automate the classification of seven distinct skin lesion categories. The study evaluates models ranging from foundational architectures (AlexNet) to modern dense-connection networks (DenseNet121).

📊 Dataset: HAM10000
The models are trained and validated using the HAM10000 ("Human Against Machine with 10,000 training images") dataset.

Total Images: 10,015 dermoscopic images.

Classes: 7 categories (Melanoma, Melanocytic nevi, Basal cell carcinoma, Actinic keratoses, Benign keratosis-like lesions, Dermatofibroma, and Vascular lesions).

Challenge: Significant class imbalance (e.g., Melanocytic Nevi comprises ~67% of the data, while others like Vascular lesions comprise only 1.4%).

🏗️ Model Architectures & Strategies
The project evaluates five architectures to analyze the evolution of computer vision in medical diagnostics:

Generation	Model	        Strategy	              Key Feature
Baseline	 AlexNet	      Trained from scratch	  5 Conv layers, 11x11 filters.
Baseline	 ZF-Net	        Trained from scratch	  Improved 7x7 filters, reduced stride.
Transfer	 InceptionV3	  Fine-tuned (ImageNet)	  Multi-scale feature extraction modules.
Transfer	 ResNet50	      Fine-tuned (ImageNet)	  Top Performer (89.1% Accuracy). Residual links.
Proposed	 DenseNet121	  Two-Phase Training	    Feature reuse via dense connections.

The Two-Phase Training Strategy (DenseNet121)
To maximize the utility of pre-trained weights on a smaller medical dataset, DenseNet121 was trained in two stages:

Phase I (Epochs 0–14): Base layers frozen. Only the custom classification head (GlobalAveragePooling2D + Dropout 0.4 + Dense Softmax) is trained.

Phase II (Epoch 15+): All layers unfrozen. The entire network is fine-tuned with a lower learning rate (1×10 
−5).

🚀 Key Results
Highest Accuracy: ResNet50 achieved the peak validation accuracy of 89.1%.

DenseNet121 Performance: Reached 82.23% validation accuracy at Epoch 49 with high stability (4.73% generalization gap).

Inference: The study demonstrates that while deeper models like ResNet50 provide superior accuracy, two-phase training in DenseNet offers a highly stable alternative for resource-constrained deployment.
