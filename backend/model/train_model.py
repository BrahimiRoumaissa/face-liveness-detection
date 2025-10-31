"""
Train MobileNetV2-based liveness detection model
"""
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import cv2
from pathlib import Path


def load_and_preprocess_dataset(data_dir, image_size=(128, 128)):
    """
    Load and preprocess dataset from directory structure:
    data_dir/
        real/
            image1.jpg
            image2.jpg
            ...
        spoof/
            image1.jpg
            image2.jpg
            ...
    """
    real_images = []
    spoof_images = []
    
    real_dir = Path(data_dir) / "real"
    spoof_dir = Path(data_dir) / "spoof"
    
    # Load real images
    if real_dir.exists():
        for img_path in real_dir.glob("*.jpg"):
            img = cv2.imread(str(img_path))
            if img is not None:
                img = cv2.resize(img, image_size)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                real_images.append(img)
    
    # Load spoof images
    if spoof_dir.exists():
        for img_path in spoof_dir.glob("*.jpg"):
            img = cv2.imread(str(img_path))
            if img is not None:
                img = cv2.resize(img, image_size)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                spoof_images.append(img)
    
    # Create labels (1 for real, 0 for spoof)
    real_labels = [1] * len(real_images)
    spoof_labels = [0] * len(spoof_images)
    
    # Combine
    X = np.array(real_images + spoof_images, dtype=np.float32) / 255.0
    y = np.array(real_labels + spoof_labels)
    
    return X, y


def create_model(input_shape=(128, 128, 3)):
    """
    Create MobileNetV2-based liveness detection model
    """
    # Load MobileNetV2 as base
    base = MobileNetV2(
        weights="imagenet",
        include_top=False,
        input_shape=input_shape
    )
    
    # Freeze base layers initially (optional - can unfreeze later for fine-tuning)
    base.trainable = False
    
    # Add custom head
    x = base.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(64, activation='relu')(x)
    x = Dropout(0.3)(x)
    out = Dense(1, activation='sigmoid')(x)
    
    model = Model(base.input, out)
    
    return model


def train_model(
    data_dir="datasets",
    model_save_path="models/liveness_model.h5",
    epochs=10,
    batch_size=32,
    validation_split=0.2,
    test_split=0.1
):
    """
    Train the liveness detection model
    """
    print("Loading dataset...")
    X, y = load_and_preprocess_dataset(data_dir)
    
    if len(X) == 0:
        print("Error: No images found in dataset directory!")
        print("Please ensure dataset structure is:")
        print("  datasets/real/*.jpg")
        print("  datasets/spoof/*.jpg")
        return None
    
    print(f"Loaded {len(X)} images ({np.sum(y)} real, {len(y) - np.sum(y)} spoof)")
    
    # Split dataset: train/val/test (70/20/10)
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_split, random_state=42, stratify=y
    )
    
    val_size = validation_split / (1 - test_split)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_size, random_state=42, stratify=y_temp
    )
    
    print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
    
    # Data augmentation
    train_datagen = ImageDataGenerator(
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    train_generator = train_datagen.flow(
        X_train, y_train,
        batch_size=batch_size
    )
    
    # Create model
    print("Creating model...")
    model = create_model()
    
    # Compile
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy', 'precision', 'recall']
    )
    
    print("Model architecture:")
    model.summary()
    
    # Callbacks
    callbacks = [
        keras.callbacks.ModelCheckpoint(
            model_save_path,
            save_best_only=True,
            monitor='val_accuracy',
            mode='max'
        ),
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7
        )
    ]
    
    # Train
    print("Training model...")
    history = model.fit(
        train_generator,
        epochs=epochs,
        validation_data=(X_val, y_val),
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate on test set
    print("\nEvaluating on test set...")
    test_loss, test_accuracy, test_precision, test_recall = model.evaluate(
        X_test, y_test, verbose=1
    )
    
    print(f"\nTest Results:")
    print(f"  Accuracy: {test_accuracy:.4f}")
    print(f"  Precision: {test_precision:.4f}")
    print(f"  Recall: {test_recall:.4f}")
    
    # Save final model
    model.save(model_save_path)
    print(f"\nModel saved to {model_save_path}")
    
    return model, history


if __name__ == "__main__":
    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)
    
    # Train model
    model, history = train_model(
        data_dir="datasets",
        model_save_path="models/liveness_model.h5",
        epochs=10,
        batch_size=32
    )

